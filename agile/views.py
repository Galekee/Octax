import csv
import json
from urllib.parse import quote
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404,redirect,render
from django.views.decorators.http import require_POST
from django.utils import timezone
from .forms import ProjectForm,SprintForm,WorkItemForm
from .models import Project,Sprint,WorkItem,StatusEvent
from .metrics import calculate,cumulative_flow

def own_project(request,pk): return get_object_or_404(Project,pk=pk,owner=request.user)
@login_required
def projects(request):
    return render(request,'agile/projects.html',{'title':'Agile','projects':Project.objects.filter(owner=request.user).annotate(item_count=Count('items'))})
@login_required
def new_project(request):
    form=ProjectForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        p=form.save(commit=False);p.owner=request.user;p.save();return redirect('agile_board',pk=p.pk)
    return render(request,'agile/form.html',{'title':'Новый Agile-проект','form':form,'back':'agile_projects'})
@login_required
def board(request,pk):
    project=own_project(request,pk)
    sprints=list(project.sprints.order_by('start_date','pk'))
    selected=request.GET.get('sprint')
    sprint=next((s for s in sprints if str(s.pk)==selected),None) if selected else (sprints[-1] if sprints else None)
    items=project.items.filter(sprint=sprint) if sprint else project.items.filter(sprint__isnull=True)
    columns=[{'key':key,'name':name,'items':list(items.filter(status=key))} for key,name in WorkItem.STATES]
    return render(request,'agile/board.html',{'title':'Kanban','project':project,'sprints':sprints,'sprint':sprint,'columns':columns})
@login_required
def new_sprint(request,pk):
    project=own_project(request,pk);form=SprintForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        obj=form.save(commit=False);obj.project=project;obj.save();return redirect('agile_board',pk=pk)
    return render(request,'agile/form.html',{'title':'Новый спринт','form':form,'project':project})
@login_required
def edit_sprint(request,pk,sid):
    project=own_project(request,pk);sprint=get_object_or_404(Sprint,pk=sid,project=project)
    form=SprintForm(request.POST or None,instance=sprint)
    if request.method=='POST' and form.is_valid(): form.save();return redirect('agile_report',pk=pk)
    return render(request,'agile/form.html',{'title':'Ретроспектива и спринт','form':form,'project':project})
@login_required
def new_item(request,pk):
    project=own_project(request,pk);form=WorkItemForm(request.POST or None,project=project)
    if request.method=='POST' and form.is_valid():
        obj=form.save(commit=False);obj.project=project;obj.save()
        StatusEvent.objects.create(item=obj,to_status=obj.status)
        return redirect('agile_board',pk=pk)
    return render(request,'agile/form.html',{'title':'Новая задача','form':form,'project':project})
@login_required
@require_POST
def move_item(request,pk,iid):
    project=own_project(request,pk)
    item=get_object_or_404(WorkItem,pk=iid,project=project)
    state=request.POST.get('status')
    allowed=[k for k,_ in WorkItem.STATES]
    if state not in allowed: return HttpResponseBadRequest('Недопустимый статус')
    with transaction.atomic():
        # Row-lock project to serialize competing moves in SQLite/Postgres as far as supported.
        Project.objects.select_for_update().get(pk=project.pk)
        item=WorkItem.objects.select_for_update().get(pk=item.pk)
        if state != item.status:
            if state==WorkItem.DOING and item.status!=WorkItem.DOING and project.items.filter(status=WorkItem.DOING).count()>=project.wip_limit:
                messages.error(request,'WIP-лимит достигнут. Завершите текущую работу.')
                return redirect('agile_board',pk=pk)
            now=timezone.now();before=item.status
            if state in (WorkItem.DOING,WorkItem.REVIEW,WorkItem.DONE) and not item.started_at: item.started_at=now
            item.status=state
            item.completed_at=now if state==WorkItem.DONE else None
            item.save(update_fields=['status','started_at','completed_at'])
            StatusEvent.objects.create(item=item,from_status=before,to_status=state,changed_at=now)
    return redirect('agile_board',pk=pk)
@login_required
def report(request,pk):
    project=own_project(request,pk)
    rows=[{'sprint':s,'metric':calculate(s),'flow_json':json.dumps(cumulative_flow(s))} for s in project.sprints.order_by('start_date')]
    return render(request,'agile/report.html',{'title':'Отчёт спринтов','project':project,'rows':rows,'flow_json':json.dumps([{'sprint':row['sprint'].name,'flow':row['flow']} for row in rows],ensure_ascii=False)})
@login_required
def report_csv(request,pk):
    project=own_project(request,pk)
    response=HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition']='attachment; filename="sprint_metrics.csv"'
    response.write('\ufeff');writer=csv.writer(response)
    writer.writerow(['Sprint','Throughput','Mean cycle days','P85 cycle days','Items'])
    for s in project.sprints.order_by('start_date'):
        m=calculate(s);writer.writerow([s.name,m['throughput'],m['mean'],m['p85'],m['total']])
    return response
