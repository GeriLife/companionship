from django.test import TestCase
from django.urls import reverse

from accounts.models import User


class PersonCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "test@user.com", 
            "test12345"
        )

    def test_anonymous_access(self):
        """Anonymous user should be redirected to login"""
        redirect_status_code = 302
        redirect_url = "/accounts/login/?next=/people/create"

        response = self.client.get(reverse("person-create"))

        self.assertEqual(response.status_code, redirect_status_code)
        self.assertEqual(response.url, redirect_url)

    def test_authenticated_access(self):
        """Authenticated user should be able to access view"""
        success_status_code = 200
        self.client.force_login(self.user)

        response = self.client.get(reverse("person-create"))

        self.assertEqual(response.status_code, success_status_code)

    def tearDown(self):
        self.user.delete()
