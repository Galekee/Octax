from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import BudgetEntry


class FinanceLab8Tests(TestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user(username='owner_lab8', password='GoodPassword123!')
        self.another = get_user_model().objects.create_user(username='another_lab8', password='GoodPassword123!')
        BudgetEntry.objects.create(owner=self.owner, month=date(2026, 10, 1), category='Сервер',
                                   planned=Decimal('120000'), actual=Decimal('90000'))
        BudgetEntry.objects.create(owner=self.another, month=date(2026, 10, 1), category='Секретные расходы',
                                   planned=Decimal('100000'), actual=Decimal('100000'))
        self.client.force_login(self.owner)

    def test_finance_dashboard_uses_only_owners_data(self):
        response = self.client.get(reverse('finance_dashboard'), {'year': '2026', 'users': '10'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['planned'], Decimal('120000'))
        self.assertEqual(response.context['actual'], Decimal('90000'))
        self.assertEqual(response.context['per_user'], Decimal('1000'))
        self.assertContains(response, 'Сервер')
        self.assertNotContains(response, 'Секретные расходы')
        self.assertEqual(len(response.context['months']), 12)

    def test_sla_calculates_error_budget(self):
        response = self.client.get(reverse('finance_sla'), {'volume': '10000'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual([s['allowed_errors'] for s in response.context['scenarios']], [50, 100, 50])
        self.assertContains(response, 'не данные живого мониторинга')

    def test_csv_export_is_scoped_to_owner(self):
        response = self.client.get(reverse('finance_export'), {'year': '2026'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Сервер', response.content.decode('utf-8-sig'))
        self.assertNotIn('Секретные расходы', response.content.decode('utf-8-sig'))

    def test_cannot_edit_another_users_entry(self):
        entry = BudgetEntry.objects.get(owner=self.another)
        self.assertEqual(self.client.get(reverse('finance_edit', args=[entry.pk])).status_code, 404)

    def test_downloads_require_authentication(self):
        self.client.logout()
        response = self.client.get(reverse('finance_document', args=['sow']))
        self.assertEqual(response.status_code, 302)

    def test_document_slugs_are_whitelisted(self):
        self.assertEqual(self.client.get(reverse('finance_document', args=['invalid'])).status_code, 404)
