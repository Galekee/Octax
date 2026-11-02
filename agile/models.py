from django.conf import settings
from django.db import models
from django.utils import timezone

class Project(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="agile_projects")
    name = models.CharField(max_length=160)
    goal = models.TextField(blank=True)
    wip_limit = models.PositiveSmallIntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name

class Sprint(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="sprints")
    name = models.CharField(max_length=120)
    goal = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    retrospective = models.TextField(blank=True)
    improvement = models.CharField(max_length=255, blank=True)
    improvement_owner = models.CharField(max_length=120, blank=True)
    def __str__(self): return self.name

class WorkItem(models.Model):
    BACKLOG='backlog'; READY='ready'; DOING='doing'; REVIEW='review'; DONE='done'
    STATES=[(BACKLOG,'Бэклог'),(READY,'К выполнению'),(DOING,'В работе'),(REVIEW,'Проверка'),(DONE,'Готово')]
    project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name='items')
    sprint = models.ForeignKey(Sprint,on_delete=models.SET_NULL,null=True,blank=True,related_name='items')
    title = models.CharField(max_length=220)
    description = models.TextField(blank=True)
    assignee = models.CharField(max_length=120,blank=True)
    status = models.CharField(max_length=12,choices=STATES,default=BACKLOG)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True,blank=True)
    completed_at = models.DateTimeField(null=True,blank=True)
    def __str__(self): return self.title

class StatusEvent(models.Model):
    item = models.ForeignKey(WorkItem,on_delete=models.CASCADE,related_name='events')
    from_status = models.CharField(max_length=12,blank=True)
    to_status = models.CharField(max_length=12)
    changed_at = models.DateTimeField(default=timezone.now)
    class Meta:
        ordering=['changed_at','pk']
