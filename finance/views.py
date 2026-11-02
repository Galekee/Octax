import csv
from datetime import date
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import BudgetEntryForm
from .models import BudgetEntry

MONTH_NAMES = ('Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
               'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь')
SLO_SCENARIOS = [
    {'name': 'Вход сотрудника', 'short': 'Авторизация', 'description': 'Успешные входы с корректными учётными данными', 'slo': Decimal('99.5'), 'sla': Decimal('99.0'), 'color': 'violet'},
    {'name': 'Открытие клиентов', 'short': 'Список клиентов', 'description': 'HTTP без ошибок, ответ не дольше одной секунды', 'slo': Decimal('99.0'), 'sla': Decimal('98.5'), 'color': 'blue'},
    {'name': 'Сохранение сделки', 'short': 'Сохранение', 'description': 'Успешные сохранения корректно заполненных сделок', 'slo': Decimal('99.5'), 'sla': Decimal('99.0'), 'color': 'green'},
]

def employee_only(request):
    return not hasattr(request.user, 'portal_profile') and not getattr(request.user, 'client_portal', False)


def positive_integer(value, default, limit=1000000):
    try:
        n = int(value)
    except (TypeError, ValueError):
        return default
    return n if 1 <= n <= limit else default


def valid_year(request):
    year = positive_integer(request.GET.get('year'), timezone.localdate().year, limit=2100)
    return year if year >= 2000 else timezone.localdate().year


@login_required
def dashboard(request):
    if not employee_only(request):
        return HttpResponseForbidden('Раздел доступен только сотрудникам')
    year = valid_year(request)
    entries = BudgetEntry.objects.filter(owner=request.user, month__year=year)
    totals = entries.aggregate(planned=Sum('planned'), actual=Sum('actual'))
    planned = totals['planned'] or Decimal('0')
    actual = totals['actual'] or Decimal('0')
    variance = planned - actual
    users = positive_integer(request.GET.get('users'), 50)
    monthly_average = planned / Decimal('12')
    per_user = monthly_average / users
    # Aggregation is one query instead of 12 separate monthly queries.
    by_month = {r['month__month']: r for r in entries.values('month__month').annotate(
        p=Sum('planned'), a=Sum('actual'))}
    raw_months = []
    for m in range(1, 13):
        values = by_month.get(m, {})
        raw_months.append({'number': m, 'name': MONTH_NAMES[m-1], 'short': MONTH_NAMES[m-1][:3],
                           'planned': values.get('p') or Decimal('0'),
                           'actual': values.get('a') or Decimal('0')})
    max_value = max([row[col] for row in raw_months for col in ('planned', 'actual')] + [Decimal('1')])
    months = []
    for row in raw_months:
        months.append({**row, 'p_height': float(row['planned'] / max_value * 100),
                       'a_height': float(row['actual'] / max_value * 100)})
    percent_used = float(actual / planned * 100) if planned > 0 else 0
    context = {
        'title': 'Финансы', 'entries': entries.order_by('-month', 'category'),
        'year': year, 'planned': planned, 'actual': actual, 'variance': variance,
        'months': months, 'users': users, 'monthly_average': monthly_average,
        'per_user': per_user, 'percent_used': percent_used,
        'percent_bar': min(percent_used, 100),
        'over_budget': planned > 0 and actual > planned,
        'has_data': bool(entries.exists()), 'entry_count': entries.count(),
        'current_year': timezone.localdate().year,
    }
    return render(request, 'finance/dashboard.html', context)


@login_required
def sla_dashboard(request):
    if not employee_only(request):
        return HttpResponseForbidden('Раздел доступен только сотрудникам')
    volume = positive_integer(request.GET.get('volume'), 10000, limit=10000000)
    scenarios = []
    for item in SLO_SCENARIOS:
        scenarios.append({**item,
            'error_percent': 100 - item['slo'],
            'allowed_errors': int(Decimal(volume) * (100 - item['slo']) / Decimal(100)),
            'sla_errors': int(Decimal(volume) * (100 - item['sla']) / Decimal(100)),
        })
    return render(request, 'finance/sla.html', {
        'title': 'SLA и качество', 'scenarios': scenarios,
        'volume': volume, 'window': '30 дней',
    })


@login_required
def export_csv(request):
    if not employee_only(request):
        return HttpResponseForbidden('Раздел доступен только сотрудникам')
    year = valid_year(request)
    entries = BudgetEntry.objects.filter(owner=request.user, month__year=year)
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="smartcrm_budget_{year}.csv"'
    response.write('\ufeff')
    writer = csv.writer(response)
    writer.writerow(['Месяц', 'Категория', 'Описание', 'План (KZT)', 'Факт (KZT)'])
    for item in entries:
        writer.writerow([item.month.strftime('%Y-%m'), item.category, item.description,
                         str(item.planned), str(item.actual)])
    return response


@login_required
def entry_form(request, pk=None):
    if not employee_only(request):
        return HttpResponseForbidden('Раздел доступен только сотрудникам')
    entry = get_object_or_404(BudgetEntry, pk=pk, owner=request.user) if pk else None
    form = BudgetEntryForm(request.POST or None, instance=entry)
    if request.method == 'POST' and form.is_valid():
        item = form.save(commit=False)
        item.owner = request.user
        item.save()
        return redirect('finance_dashboard')
    return render(request, 'finance/form.html', {
        'title': 'Редактирование бюджета' if entry else 'Новая статья бюджета',
        'form': form, 'entry': entry,
    })


@login_required
def entry_delete(request, pk):
    if not employee_only(request):
        return HttpResponseForbidden('Раздел доступен только сотрудникам')
    entry = get_object_or_404(BudgetEntry, pk=pk, owner=request.user)
    if request.method == 'POST':
        entry.delete()
        return redirect('finance_dashboard')
    return render(request, 'finance/delete.html', {'title': 'Удалить статью', 'entry': entry})


@login_required
def document_download(request, slug):
    """Small, explicitly allowlisted document endpoint; never accept file paths."""
    from django.http import Http404
    if slug != 'sow':
        raise Http404('Документ не найден')
    response = HttpResponse(
        'OCTAX — шаблон технического задания\n\n'
        'Проект: __________________\n'
        'Объём работ: __________________\n'
        'Сроки: __________________\n',
        content_type='text/plain; charset=utf-8',
    )
    response['Content-Disposition'] = 'attachment; filename="octax-sow-template.txt"'
    return response
