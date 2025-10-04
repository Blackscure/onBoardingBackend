from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from role.api.serilizers import RoleSerializer
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


class RoleSerializerTest(TestCase):
    def setUp(self):
        self.role_data = {"role_name": "Editor", "description": "Can edit content"}
        self.role = Role.objects.create(**self.role_data)
        self.serializer = RoleSerializer(instance=self.role)

    def test_serializer_fields(self):
        data = self.serializer.data
        self.assertEqual(data["role_name"], self.role_data["role_name"])
        self.assertEqual(data["description"], self.role_data["description"])


class RoleAPITest(APITestCase):
    def setUp(self):
        self.role = Role.objects.create(role_name="Viewer", description="Can only view")
        self.list_url = reverse("role-list-create")
        self.detail_url = reverse("role-detail", kwargs={"pk": self.role.id})

    def test_list_roles(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_role(self):
        response = self.client.post(self.list_url, {"role_name": "Tester", "description": "Testing only"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_role(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_role(self):
        edit_url = reverse("EditRoleAPIView", kwargs={"pk": self.role.id})
        response = self.client.put(edit_url, {"role_name": "Updated", "description": "Updated role"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete_role(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
