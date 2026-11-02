from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from crm.models import Client
from .models import Company, Lead

class SalesTests(TestCase):
    def setUp(self):
        U=get_user_model()
        self.a=U.objects.create_user(username='alpha',password='testpass123')
        self.b=U.objects.create_user(username='beta',password='testpass123')
        self.company=Company.objects.create(owner=self.a,name='Acme')
        self.lead=Lead.objects.create(owner=self.a,name='Alice',company=self.company)
        self.client.force_login(self.a)
    def test_lists(self):
        for kind in ('leads','companies'):
            self.assertEqual(self.client.get(reverse('sales_list',args=[kind])).status_code,200)
    def test_cross_user_edit_blocked(self):
        self.client.force_login(self.b)
        self.assertEqual(self.client.get(reverse('sales_edit',args=['leads',self.lead.pk])).status_code,404)
        self.assertEqual(self.client.post(reverse('sales_delete',args=['companies',self.company.pk])).status_code,404)
    def test_cross_user_company_cannot_be_assigned(self):
        self.client.force_login(self.b)
        r=self.client.post(reverse('sales_create',args=['leads']),{'name':'Bob','company':self.company.pk,'status':'new','source':'other'})
        self.assertEqual(r.status_code,200)
        self.assertFalse(Lead.objects.filter(owner=self.b).exists())
    def test_conversion_once(self):
        url=reverse('sales_convert',args=[self.lead.pk])
        self.assertEqual(self.client.post(url).status_code,302)
        self.assertEqual(self.client.post(url).status_code,302)
        self.assertEqual(Client.objects.filter(owner=self.a,name='Alice').count(),1)
        self.lead.refresh_from_db()
        self.assertEqual(self.lead.status,Lead.Status.CONVERTED)
    def test_conversion_requires_post(self):
        self.assertEqual(self.client.get(reverse('sales_convert',args=[self.lead.pk])).status_code,405)
    def test_login_required(self):
        self.client.logout()
        self.assertEqual(self.client.get(reverse('sales_list',args=['leads'])).status_code,302)
