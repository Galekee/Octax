from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseForbidden, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from crm.models import Client
from crm.views import crm_user_required
from .models import Lead, Company
from .forms import LeadForm, CompanyForm

CONFIG = {'leads': (Lead, LeadForm, 'Лиды'), 'companies': (Company, CompanyForm, 'Компании')}

@crm_user_required
def listing(request, kind):
    if kind not in CONFIG: raise Http404()
    model, _, title = CONFIG[kind]
    qs = model.objects.filter(owner=request.user)
    query = request.GET.get('q','').strip()[:150]
    if query:
        qs = qs.filter(Q(name__icontains=query) | Q(email__icontains=query) | Q(phone__icontains=query))
    status = request.GET.get('status','')
    if kind == 'leads' and status in Lead.Status.values:
        qs = qs.filter(status=status)
    return render(request, 'sales/list.html', {'items': qs[:100], 'title': title, 'kind':kind, 'query':query, 'status':status, 'statuses': Lead.Status.choices if kind=='leads' else []})

@crm_user_required
def edit(request, kind, pk=None):
    if kind not in CONFIG: raise Http404()
    model, form_class, title = CONFIG[kind]
    instance = get_object_or_404(model, pk=pk, owner=request.user) if pk else None
    if request.method == 'POST' and instance and kind == 'leads' and instance.status == Lead.Status.CONVERTED:
        return HttpResponseForbidden('Преобразованный лид недоступен для редактирования')
    kwargs = {'instance':instance}
    if kind == 'leads': kwargs['owner'] = request.user
    form = form_class(request.POST or None, **kwargs)
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        obj.owner = request.user
        obj.save()
        messages.success(request, 'Запись сохранена')
        return redirect('sales_list', kind=kind)
    return render(request,'sales/form.html', {'form':form, 'title':('Изменить ' if pk else 'Добавить ') + ('лида' if kind=='leads' else 'компанию'), 'kind':kind})

@crm_user_required
@require_POST
def delete(request, kind, pk):
    if kind not in CONFIG: raise Http404()
    model, _, _ = CONFIG[kind]
    obj = get_object_or_404(model, pk=pk, owner=request.user)
    if kind == 'leads' and obj.status == Lead.Status.CONVERTED:
        return HttpResponseForbidden('Нельзя удалить преобразованный лид')
    obj.delete()
    messages.success(request,'Запись удалена')
    return redirect('sales_list', kind=kind)

@crm_user_required
@require_POST
@transaction.atomic
def convert_lead(request, pk):
    lead = get_object_or_404(Lead.objects.select_for_update(), pk=pk, owner=request.user)
    if lead.converted_client_id:
        messages.info(request,'Этот лид уже преобразован')
        return redirect('sales_list', kind='leads')
    client = Client.objects.create(owner=request.user, name=lead.name, email=lead.email,
        phone=lead.phone, company=lead.company.name if lead.company else '', notes=lead.notes)
    lead.converted_client = client
    lead.status = Lead.Status.CONVERTED
    lead.save(update_fields=['converted_client','status'])
    messages.success(request,'Лид преобразован в клиента')
    return redirect('clients_detail', pk=client.pk)
