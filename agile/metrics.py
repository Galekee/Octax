from datetime import timedelta
from statistics import mean
from django.utils import timezone
from .models import WorkItem

def percentile85(values):
    if not values: return None
    seq=sorted(values)
    from math import ceil
    return round(seq[max(0,ceil(.85*len(seq))-1)],2)

def calculate(sprint):
    items=list(sprint.items.prefetch_related('events'))
    done=[x for x in items if x.completed_at and x.status==WorkItem.DONE]
    durations=[(x.completed_at - (x.started_at or x.created_at)).total_seconds()/86400 for x in done]
    return {'total':len(items),'done':len(done),'throughput':len(done),'mean':round(mean(durations),2) if durations else None,'p85':percentile85(durations)}

def cumulative_flow(sprint):
    # Event timeline: each day ending at 23:59:59 in the configured local time zone.
    items=list(sprint.items.prefetch_related('events'))
    today=timezone.localdate()
    last=min(sprint.end_date,today)
    if last<sprint.start_date: return []
    result=[]; day=sprint.start_date
    while day<=last:
        counts={key:0 for key,_ in WorkItem.STATES}
        cutoff=day+timedelta(days=1)
        for item in items:
            if timezone.localtime(item.created_at).date()>=cutoff: continue
            state=WorkItem.BACKLOG
            for event in item.events.all():
                if timezone.localtime(event.changed_at).date() < cutoff: state=event.to_status
            counts[state]+=1
        result.append({'day':day.isoformat(),**counts})
        day+=timedelta(days=1)
    return result
