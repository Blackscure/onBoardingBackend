from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from role.models import Role

class RoleAPITestCase(APITestCase):
    def setUp(self):
        self.role = Role.objects.create(
            role_name="Developer",
            description="Writes and maintains code"
        )
        self.list_url = reverse("role-list-create")
        self.detail_url = reverse("role-detail", kwargs={"pk": self.role.pk})
        self.edit_url = reverse("EditRoleAPIView", kwargs={"pk": self.role.pk})

    def test_get_roles_list(self):
        """GET /roles/ should return all roles"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Developer", str(response.data))

    def test_create_role(self):
        """POST /roles/ should create a new role"""
        data = {"role_name": "Tester", "description": "Ensures software quality"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Role.objects.count(), 2)

    def test_get_role_detail(self):
        """GET /roles/<id>/ should return a single role"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["role_name"], "Developer")

    def test_edit_role(self):
        """PUT /edit-role/<id>/ should update a role"""
        data = {"role_name": "Senior Developer", "description": "Builds systems"}
        response = self.client.put(self.edit_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.role.refresh_from_db()
        self.assertEqual(self.role.role_name, "Senior Developer")

    def test_delete_role(self):
        """DELETE /roles/<id>/ should delete a role"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Role.objects.count(), 0)
