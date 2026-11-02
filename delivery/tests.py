from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch

class OctaxBrandingTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="qa_tester", password="safe-test-password-123")
        self.client.force_login(self.user)

    @patch("delivery.views.github_json", return_value={"workflow_runs": []})
    def test_qa_page_has_current_brand_and_repo(self, _github):
        response = self.client.get(reverse("delivery_dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Galekee/Octax")
        self.assertNotContains(response, "ЛАБОРАТОРНАЯ")
        self.assertNotContains(response, "smart-crm-system")

    def test_projects_page_no_lab_branding(self):
        response = self.client.get(reverse("agile_projects"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "ЛАБОРАТОРНАЯ")
        self.assertNotContains(response, "SMARTCRM")

    def test_finance_page_no_broken_document_links(self):
        response = self.client.get(reverse("finance_dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "finance/documents/")
        self.assertNotContains(response, "ЛЗ №8")
