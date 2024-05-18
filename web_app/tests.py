from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Records

class TestRegisterView(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')

    def test_register_view(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web_app/register.html')

        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'password1': 'newpassword',
            'password2': 'newpassword',
        })
        self.assertIn(response.status_code, [200, 302])

        response = self.client.post(self.register_url, {})
        self.assertEqual(response.status_code, 200) 

class TestLoginView(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('my_login')
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login_view(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web_app/my-login.html')

        # Test login with valid credentials
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword',
        })
        self.assertEqual(response.status_code, 302)  # Redirect on success

        # Test login with invalid credentials
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)  # Form is not valid, stays on the same page

# Similar test classes for other views: Dashboard, Logout, CreateRecord, UpdateRecord,
# SingularRecord, DeleteRecord
