from django.test import TestCase
from role.models import Role
from role.serializers import RoleSerializer

class RoleSerializerTest(TestCase):
    def setUp(self):
        self.role_data = {
            "role_name": "Manager",
            "description": "Handles team operations"
        }
        self.role = Role.objects.create(**self.role_data)
        self.serializer = RoleSerializer(instance=self.role)

    def test_contains_expected_fields(self):
        """Serializer should include all model fields"""
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(),
            ["id", "role_name", "description", "created_at", "updated_at"]
        )

    def test_field_content(self):
        """Serializer should correctly serialize model fields"""
        data = self.serializer.data
        self.assertEqual(data["role_name"], self.role.role_name)
        self.assertEqual(data["description"], self.role.description)

    def test_serializer_create(self):
        """Test serializer can create a Role"""
        serializer = RoleSerializer(data=self.role_data)
        self.assertTrue(serializer.is_valid())
        role = serializer.save()
        self.assertEqual(role.role_name, "Manager")
