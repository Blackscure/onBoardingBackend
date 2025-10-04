from django.test import TestCase
from role.models import Role

class RoleModelTest(TestCase):
    def setUp(self):
        self.role = Role.objects.create(
            role_name="Admin",
            description="Administrator role with full permissions"
        )

    def test_role_creation(self):
        """Test that a role instance is created successfully"""
        self.assertEqual(self.role.role_name, "Admin")
        self.assertEqual(self.role.description, "Administrator role with full permissions")

    def test_str_method(self):
        """Test the string representation of a Role"""
        self.assertEqual(str(self.role), "Admin")

    def test_auto_timestamps(self):
        """Test that created_at and updated_at are auto populated"""
        self.assertIsNotNone(self.role.created_at)
        self.assertIsNotNone(self.role.updated_at)
