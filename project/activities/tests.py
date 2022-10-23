from http import HTTPStatus

from circles.models import Circle, Companion
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Activity

User = get_user_model()


class ActivityCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "test@user.com",
            "test12345",
        )
        self.user_without_circle = User.objects.create_user(
            "test_two@user.com",
            "test12345",
        )
        self.circle_without_companion = Circle.objects.create(
            name="Non-companion circle"
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
        response = self.client.get(reverse("activity-create"))

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_anonymous_access(self):
        """Anonymous user should not be authorized"""
        response = self.client.post(
            reverse("activity-create"),
            follow=True,
        )

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_authenticated_non_companion_activity_create(self):
        """Authenticated user who is not companion should not be authorized"""
        self.client.force_login(self.user_without_circle)

        response = self.client.post(
            reverse("activity-create"),
            {
                "activity_type": Activity.ActivityTypeChoices.APPOINTMENT,
                "activity_date": "2022-10-23",
                "circle": self.circle_with_companion.id,
            },
            follow=True,
        )

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_authenticated_companion_activity_create(self):
        """Authenticated user who is not companion should not be authorized"""
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("activity-create"),
            {
                "activity_type": Activity.ActivityTypeChoices.APPOINTMENT,
                "activity_date": "2022-10-23",
                "circle": self.circle_with_companion.id,
            },
            follow=True,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)


class ActivityUpdateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "test@user.com",
            "test12345",
        )
        self.user_without_circle = User.objects.create_user(
            "test_two@user.com",
            "test12345",
        )

        # This circle will have the user as a companion
        self.circle_with_companion = Circle.objects.create(name="Companion circle")
        self.companionship_through = Companion.objects.create(
            circle=self.circle_with_companion, user=self.user
        )
        self.activity_for_circle_with_companion = Activity.objects.create(
            activity_type=Activity.ActivityTypeChoices.APPOINTMENT,
            activity_date="2022-10-23",
            circle=self.circle_with_companion,
        )

    def test_get_http_method_should_fail(self):
        """GET request should not be allowed"""
        response = self.client.get(
            reverse(
                "activity-update",
                kwargs={
                    "pk": self.activity_for_circle_with_companion.id,
                },
            ),
        )

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_anonymous_access(self):
        """Anonymous user should not be authorized"""
        response = self.client.post(
            reverse(
                "activity-update",
                kwargs={
                    "pk": self.activity_for_circle_with_companion.id,
                },
            ),
        )

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_authenticated_non_companion_activity_create(self):
        """Authenticated user who is not companion should not be authorized"""
        self.client.force_login(self.user_without_circle)

        response = self.client.post(
            reverse(
                "activity-update",
                kwargs={
                    "pk": self.activity_for_circle_with_companion.id,
                },
            ),
            {
                "activity_type": Activity.ActivityTypeChoices.APPOINTMENT,
                "activity_date": "2022-10-23",
                "circle": self.circle_with_companion.id,
            },
            follow=True,
        )

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_authenticated_companion_activity_create(self):
        """Authenticated user who is not companion should not be authorized"""
        self.client.force_login(self.user)

        response = self.client.post(
            reverse(
                "activity-update",
                kwargs={
                    "pk": self.activity_for_circle_with_companion.id,
                },
            ),
            {
                "activity_type": Activity.ActivityTypeChoices.APPOINTMENT,
                "activity_date": "2022-10-23",
                "circle": self.circle_with_companion.id,
            },
            follow=True,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)


class ActivityDeleteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "test@user.com",
            "test12345",
        )
        self.user_without_circle = User.objects.create_user(
            "test_two@user.com",
            "test12345",
        )

        # This circle will have the user as a companion
        self.circle_with_companion = Circle.objects.create(name="Companion circle")
        self.companionship_through = Companion.objects.create(
            circle=self.circle_with_companion,
            user=self.user,
            is_organizer=True,
        )
        self.activity_for_circle_with_companion = Activity.objects.create(
            activity_type=Activity.ActivityTypeChoices.APPOINTMENT,
            activity_date="2022-10-23",
            circle=self.circle_with_companion,
        )

    def test_get_http_method_should_fail(self):
        """GET request should not be allowed"""
        response = self.client.get(
            reverse(
                "activity-delete",
                kwargs={
                    "activity_id": self.activity_for_circle_with_companion.id,
                },
            ),
        )

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_anonymous_access(self):
        """Anonymous user should not be authorized"""
        response = self.client.post(
            reverse(
                "activity-delete",
                kwargs={
                    "activity_id": self.activity_for_circle_with_companion.id,
                },
            ),
        )

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_authenticated_non_companion_activity_delete(self):
        """Authenticated user who is not companion should not be authorized"""
        self.client.force_login(self.user_without_circle)

        response = self.client.post(
            reverse(
                "activity-delete",
                kwargs={
                    "activity_id": self.activity_for_circle_with_companion.id,
                },
            ),
        )

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_authenticated_companion_activity_delete(self):
        """Authenticated user who is not companion should not be authorized"""
        self.client.force_login(self.user)

        response = self.client.post(
            reverse(
                "activity-delete",
                kwargs={
                    "activity_id": self.activity_for_circle_with_companion.id,
                },
            ),
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)


class ActivityModelTest(TestCase):
    def setUp(self):

        self.companion_one = User.objects.create_user("test_one@user.com", "test12345")
        self.companion_two = User.objects.create_user("test_two@user.com", "test12345")
        self.user_three = User.objects.create_user("test_three@user.com", "test12345")

        self.circle = Circle.objects.create(name="Test circle")

        Companion.objects.create(
            circle=self.circle,
            user=self.companion_one,
        )
        Companion.objects.create(
            circle=self.circle,
            user=self.companion_two,
        )

        self.activity = Activity.objects.create(
            activity_type=Activity.ActivityTypeChoices.APPOINTMENT,
            activity_date="2022-10-23",
            circle=self.circle,
        )

    def test_remaining_eligible_companions(self):
        self.activity.participants.add(self.companion_one)

        remaining_eligible_companions = self.activity.remaining_eligible_companions

        # User already in participants list should not be eligible
        assert self.companion_one not in remaining_eligible_companions

        assert self.companion_two in remaining_eligible_companions
        assert list(remaining_eligible_companions) == [self.companion_two]

        # Non-companion should not be in eligible companions list
        assert self.user_three not in remaining_eligible_companions
