from accounts.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Circle, Companion


class CircleCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("test@user.com", "test12345")

    def test_anonymous_access(self):
        """Anonymous user should be redirected to login"""
        redirect_url = "/accounts/login/?next=/circles/create"

        response = self.client.get(reverse("circle-create"))

        self.assertRedirects(response, redirect_url)

    def test_authenticated_access(self):
        """Authenticated user should be able to access view"""
        success_status_code = 200
        self.client.force_login(self.user)

        response = self.client.get(reverse("circle-create"))

        self.assertEqual(response.status_code, success_status_code)

    def tearDown(self):
        self.user.delete()


class CircleDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("test@user.com", "test12345")
        # This circle won't have any companion
        self.circle_without_companion = Circle.objects.create(
            name="Non-companion circle"
        )
        self.circle_without_companion_detail_url = reverse(
            "circle-detail", kwargs={"pk": self.circle_without_companion.id}
        )

        # This circle will have the user as a companion
        self.circle_with_companion = Circle.objects.create(name="Companion circle")
        self.companionship_through = Companion.objects.create(
            circle=self.circle_with_companion, user=self.user
        )
        self.circle_with_companion_detail_url = reverse(
            "circle-detail", kwargs={"pk": self.circle_with_companion.id}
        )

    def test_anonymous_access(self):
        """Anonymous user should see not found error"""
        not_found_status_code = 404

        response = self.client.get(self.circle_without_companion)

        self.assertEqual(response.status_code, not_found_status_code)

    def test_authenticated_non_companion_access(self):
        """
        Authenticated user should see erro when accessing to
        whom they aren't a companion
        """
        not_authorized_status_code = 403
        self.client.force_login(self.user)

        response = self.client.get(self.circle_without_companion_detail_url)

        self.assertEqual(response.status_code, not_authorized_status_code)

    def test_authenticated_companion_access(self):
        """Authenticated user should be able to access
        a circle to whom they are a companion"""
        success_status_code = 200
        self.client.force_login(self.user)

        response = self.client.get(self.circle_with_companion_detail_url)

        self.assertEqual(response.status_code, success_status_code)

    def tearDown(self):
        self.companionship_through.delete()
        self.user.delete()
        self.circle_with_companion.delete()
        self.circle_without_companion.delete()


class CircleListViewTest(TestCase):
    def setUp(self):
        self.circle_list_url = reverse("circle-list")
        self.user_without_companion = User.objects.create_user(
            "user_without_companion@user.com", "test12345"
        )
        self.user_with_companion = User.objects.create_user(
            "user_with_companion@user.com", "test12345"
        )
        # This circle won't have any companion
        self.circle_without_companion_name = "Circle without companion"
        self.circle_without_companion = Circle.objects.create(
            name=self.circle_without_companion_name
        )

        # This circle will have the user as a companion
        self.circle_with_companion_name = "Circle with companion"
        self.circle_with_companion = Circle.objects.create(
            name=self.circle_with_companion_name
        )
        self.companionship_through = Companion.objects.create(
            circle=self.circle_with_companion, user=self.user_with_companion
        )

    def test_anonymous_access(self):
        """Anonymous user should be redirected to login with circle list as next URL"""
        redirect_url = "/accounts/login/?next=/circles/"

        response = self.client.get(self.circle_list_url)

        self.assertRedirects(response, redirect_url)

    def test_authenticated_user_without_companion(self):
        """
        Authenticated user without any companion should not see circles in the list
        """
        success_status_code = 200
        self.client.force_login(self.user_without_companion)

        response = self.client.get(self.circle_list_url)

        # User should be able to access the circles list
        self.assertEqual(response.status_code, success_status_code)

        # Circles list should not contain any existing circles
        self.assertNotContains(response, self.circle_with_companion_name)
        self.assertNotContains(response, self.circle_without_companion_name)

    def test_authenticated_user_with_companion(self):
        """Authenticated user should be able to see
        a circle to whom they are a companion"""
        success_status_code = 200
        self.client.force_login(self.user_with_companion)

        response = self.client.get(self.circle_list_url)

        # User should be able to access the circles list
        self.assertEqual(response.status_code, success_status_code)

        # Circles list should not contain any existing circles
        self.assertContains(response, self.circle_with_companion_name)
        self.assertNotContains(response, self.circle_without_companion_name)
