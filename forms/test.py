from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Form, Field

User = get_user_model()


class FormAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")

    def test_create_form(self):
        url = reverse('form-list-create')
        data = {'name': 'KYC Form', 'description': 'Know your customer form'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Form.objects.count(), 1)

    def test_get_forms(self):
        Form.objects.create(user=self.user, name="Loan Form")
        url = reverse('form-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class FieldAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="fielduser", password="password")
        self.client.login(username="fielduser", password="password")
        self.form = Form.objects.create(user=self.user, name="Registration Form")

    def test_create_field(self):
        url = reverse('field-list-create')
        data = {
            "form": str(self.form.id),
            "name": "email",
            "label": "Email Address",
            "type": "email",
            "required": True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Field.objects.count(), 1)

    def test_get_fields(self):
        Field.objects.create(
            form=self.form,
            name="first_name",
            label="First Name",
            type="text"
        )
        url = reverse('field-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
