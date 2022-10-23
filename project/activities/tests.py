from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from circles.models import Circle, Companion


class ActivityCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("test@user.com", "test12345")
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

    def test_get_http_method_should_fail(self):
        """GET request should not be allowed"""
        redirect_url = "/accounts/login/?next=/circles/create"

        response = self.client.get(reverse("activity-create"))

        # Should get HTTP 405 Method Not Allowed
        self.assertEquals(response.status_code, 405)

    def test_anonymous_access(self):
        """Anonymous user should not be authorized"""
        response = self.client.post(
            reverse("activity-create"),
            follow=True,
        )

        # Should get HTTP 403 Not Authorized
        self.assertEquals(response.status_code, 403)
