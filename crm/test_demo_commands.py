from io import StringIO
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from crm.models import Client, Deal, Task
from sales.models import Company, Lead


class DemoCommandsTests(TestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user(username="qa_owner", password="test-only-password")
        self.other = get_user_model().objects.create_user(username="other", password="test-only-password")

    def seed(self, **kwargs):
        call_command("seed_demo", user="qa_owner", batch="qa", companies=2, clients=3, leads=4, deals=2, tasks=2, stdout=StringIO(), **kwargs)

    def test_create_preview_and_delete_only_demo(self):
        real = Client.objects.create(owner=self.owner, name="Настоящий клиент")
        other = Client.objects.create(owner=self.other, name="Другой пользователь")
        self.seed()
        self.assertEqual(Company.objects.filter(owner=self.owner).count(), 2)
        self.assertEqual(Lead.objects.filter(owner=self.owner).count(), 4)
        self.assertEqual(Deal.objects.filter(owner=self.owner).count(), 2)
        self.assertEqual(Task.objects.filter(owner=self.owner).count(), 2)
        call_command("clear_demo", user="qa_owner", batch="qa", stdout=StringIO())
        self.assertEqual(Client.objects.filter(owner=self.owner).count(), 4)
        call_command("clear_demo", user="qa_owner", batch="qa", confirm=True, stdout=StringIO())
        self.assertEqual(list(Client.objects.filter(owner=self.owner)), [real])
        self.assertTrue(Client.objects.filter(pk=other.pk).exists())

    def test_duplicate_batch_is_rejected(self):
        self.seed()
        with self.assertRaises(CommandError):
            self.seed()

    def test_cleanup_refuses_real_deal_linked_to_demo_client(self):
        self.seed()
        demo_client = Client.objects.filter(owner=self.owner, notes="[OCTAX-DEMO:qa]").first()
        Deal.objects.create(owner=self.owner, client=demo_client, title="Настоящая сделка")
        with self.assertRaises(CommandError):
            call_command("clear_demo", user="qa_owner", batch="qa", confirm=True, stdout=StringIO())
        self.assertEqual(Client.objects.filter(owner=self.owner, notes="[OCTAX-DEMO:qa]").count(), 3)
