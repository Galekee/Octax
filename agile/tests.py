from datetime import date, timedelta
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .metrics import calculate, percentile85
from .models import Project, Sprint, WorkItem, StatusEvent

class AgileTests(TestCase):
    def setUp(self):
        self.owner=get_user_model().objects.create_user(username='agile_owner',password='a-long-password-123')
        self.other=get_user_model().objects.create_user(username='agile_other',password='a-long-password-123')
        self.project=Project.objects.create(owner=self.owner,name='Sample',wip_limit=1)
        today=timezone.localdate()
        self.sprint=Sprint.objects.create(project=self.project,name='Sprint 1',goal='Complete feature',start_date=today-timedelta(days=1),end_date=today+timedelta(days=7))
        self.client.force_login(self.owner)
    def test_requires_authentication(self):
        self.client.logout()
        response=self.client.get(reverse('agile_projects'))
        self.assertEqual(response.status_code,302)
    def test_isolation(self):
        self.client.force_login(self.other)
        self.assertEqual(self.client.get(reverse('agile_board',args=[self.project.pk])).status_code,404)
    def test_wip_and_history(self):
        first=WorkItem.objects.create(project=self.project,sprint=self.sprint,title='One')
        second=WorkItem.objects.create(project=self.project,sprint=self.sprint,title='Two')
        url=lambda item:reverse('agile_move_item',args=[self.project.pk,item.pk])
        self.client.post(url(first),{'status':'doing'})
        self.client.post(url(second),{'status':'doing'})
        first.refresh_from_db();second.refresh_from_db()
        self.assertEqual(first.status,'doing')
        self.assertEqual(second.status,'backlog')
        self.assertEqual(StatusEvent.objects.filter(item=first).count(),1)
        self.client.post(url(first),{'status':'done'})
        self.assertEqual(calculate(self.sprint)['throughput'],1)
    def test_invalid_move(self):
        item=WorkItem.objects.create(project=self.project,title='Item')
        response=self.client.post(reverse('agile_move_item',args=[self.project.pk,item.pk]),{'status':'oops'})
        self.assertEqual(response.status_code,400)
    def test_p85(self):
        self.assertIsNone(percentile85([]))
        self.assertEqual(percentile85([1,2,3,4,5,6,7,8,9,10]),9)
    def test_csv(self):
        response=self.client.get(reverse('agile_report_csv',args=[self.project.pk]))
        self.assertEqual(response.status_code,200)
        self.assertIn(b'Sprint',response.content)
