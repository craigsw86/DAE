from django.test import TestCase
from django.contrib.auth.models import User
from .models import RegulationUpdate, ChecklistItem
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

# Create your tests here.

class ManualRegulationAdditionTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_manual_regulation_addition_from_hhs_email(self):
        # Simulate HHS email content
        hhs_email_title = "HHS HIPAA Update: New Security Rule"
        hhs_email_description = "Effective immediately, all covered entities must implement new encryption standards."
        hhs_email_url = "https://www.hhs.gov/hipaa/for-professionals/security/guidance/index.html"

        # Admin manually adds regulation update
        regulation = RegulationUpdate.objects.create(
            title=hhs_email_title,
            description=hhs_email_description,
            source_url=hhs_email_url
        )

        # Admin assigns checklist item to user
        checklist_item = ChecklistItem.objects.create(
            user=self.user,
            regulation_update=regulation,
            completed=False,
            notes="Initial assignment from HHS update."
        )

        # Assertions
        self.assertEqual(RegulationUpdate.objects.count(), 1)
        self.assertEqual(ChecklistItem.objects.count(), 1)
        self.assertEqual(regulation.title, hhs_email_title)
        self.assertEqual(regulation.description, hhs_email_description)
        self.assertEqual(checklist_item.user.username, 'testuser')
        self.assertFalse(checklist_item.completed)
        self.assertIn("HHS", regulation.title)

class ChecklistItemRawSQLTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='rawuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.regulation = RegulationUpdate.objects.create(
            title="Raw SQL Test",
            description="Testing raw SQL endpoint.",
            source_url="https://example.com"
        )
        ChecklistItem.objects.create(
            user=self.user,
            regulation_update=self.regulation,
            completed=False,
            notes="Raw SQL note"
        )

    def test_my_items_raw_endpoint(self):
        response = self.client.get('/api/checklist/my_items_raw/')
        print("RESPONSE DATA:", response.data)  # Debug print
        self.assertEqual(response.status_code, 200)
        # The notes field is encrypted at rest, so the raw SQL returns the encrypted value.
        # We only check that the item exists, not the plaintext value.
        self.assertTrue(
            len(response.data) > 0,
            f"Expected at least one checklist item, got: {response.data}"
        )

