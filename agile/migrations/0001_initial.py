# Generated for SmartCRM Agile Lab 9
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name='Project', fields=[
            ('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
            ('name',models.CharField(max_length=160)),('goal',models.TextField(blank=True)),
            ('wip_limit',models.PositiveSmallIntegerField(default=3)),
            ('created_at',models.DateTimeField(auto_now_add=True)),
            ('owner',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='agile_projects',to=settings.AUTH_USER_MODEL))]),
        migrations.CreateModel(name='Sprint',fields=[
            ('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
            ('name',models.CharField(max_length=120)),('goal',models.TextField()),
            ('start_date',models.DateField()),('end_date',models.DateField()),
            ('retrospective',models.TextField(blank=True)),('improvement',models.CharField(blank=True,max_length=255)),
            ('improvement_owner',models.CharField(blank=True,max_length=120)),
            ('project',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='sprints',to='agile.project'))]),
        migrations.CreateModel(name='WorkItem',fields=[
            ('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
            ('title',models.CharField(max_length=220)),('description',models.TextField(blank=True)),
            ('assignee',models.CharField(blank=True,max_length=120)),
            ('status',models.CharField(choices=[('backlog','Бэклог'),('ready','К выполнению'),('doing','В работе'),('review','Проверка'),('done','Готово')],default='backlog',max_length=12)),
            ('created_at',models.DateTimeField(auto_now_add=True)),
            ('started_at',models.DateTimeField(blank=True,null=True)),('completed_at',models.DateTimeField(blank=True,null=True)),
            ('project',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='items',to='agile.project')),
            ('sprint',models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.SET_NULL,related_name='items',to='agile.sprint'))]),
        migrations.CreateModel(name='StatusEvent',fields=[
            ('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
            ('from_status',models.CharField(blank=True,max_length=12)),('to_status',models.CharField(max_length=12)),
            ('changed_at',models.DateTimeField(default=django.utils.timezone.now)),
            ('item',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='events',to='agile.workitem'))],
            options={'ordering':['changed_at','pk']}),
    ]
