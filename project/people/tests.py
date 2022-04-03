from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from people.models import Person, Companion


class PersonCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "test@user.com", 
            "test12345"
        )

    def test_anonymous_access(self):
        """Anonymous user should be redirected to login"""
        redirect_url = "/accounts/login/?next=/people/create"

        response = self.client.get(reverse("person-create"))

        self.assertRedirects(response, redirect_url)

    def test_authenticated_access(self):
        """Authenticated user should be able to access view"""
        success_status_code = 200
        self.client.force_login(self.user)

        response = self.client.get(reverse("person-create"))

        self.assertEqual(response.status_code, success_status_code)

    def tearDown(self):
        self.user.delete()


class PersonDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "test@user.com", 
            "test12345"
        )
        # This person won't have any companion
        self.person_without_companion = Person.objects.create(
            name="Non-companion person"
        )
        self.person_without_companion_detail_url = reverse("person-detail", kwargs={"pk": self.person_without_companion.id})

        # This person will have the user as a companion
        self.person_with_companion = Person.objects.create(
            name="Companion person"
        )
        self.companionship_through = Companion.objects.create(
            person=self.person_with_companion,
            user=self.user
        )
        self.person_with_companion_detail_url = reverse("person-detail", kwargs={"pk": self.person_with_companion.id})

    def test_anonymous_access(self):
        """Anonymous user should see not found error"""
        not_found_status_code = 404

        response = self.client.get(self.person_without_companion)

        self.assertEqual(response.status_code, not_found_status_code)

    def test_authenticated_non_companion_access(self):
        """Authenticated user should see erro when accessing to whom they aren't a companion"""
        not_authorized_status_code = 403
        self.client.force_login(self.user)

        response = self.client.get(self.person_without_companion_detail_url)

        self.assertEqual(response.status_code, not_authorized_status_code)

    def test_authenticated_companion_access(self):
        """Authenticated user should be able to access person to whom they are a companion"""
        success_status_code = 200
        self.client.force_login(self.user)

        response = self.client.get(self.person_with_companion_detail_url)

        self.assertEqual(response.status_code, success_status_code)

    def tearDown(self):
        self.companionship_through.delete()
        self.user.delete()
        self.person_with_companion.delete()
        self.person_without_companion.delete()


class PersonListViewTest(TestCase):
    def setUp(self):
        self.person_list_url = reverse("person-list")
        self.user_without_companion = User.objects.create_user(
            "user_without_companion@user.com", 
            "test12345"
        )
        self.user_with_companion = User.objects.create_user(
            "user_with_companion@user.com", 
            "test12345"
        )
        # This person won't have any companion
        self.person_without_companion_name = "Person without companion"
        self.person_without_companion = Person.objects.create(
            name=self.person_without_companion_name
        )

        # This person will have the user as a companion
        self.person_with_companion_name = "Person with companion"
        self.person_with_companion = Person.objects.create(
            name=self.person_with_companion_name
        )
        self.companionship_through = Companion.objects.create(
            person=self.person_with_companion,
            user=self.user_with_companion
        )

    def test_anonymous_access(self):
        """Anonymous user should be redirected to login with person list as next URL"""
        redirect_url = "/accounts/login/?next=/people/"

        response = self.client.get(self.person_list_url)

        self.assertRedirects(response, redirect_url)

    def test_authenticated_user_without_companion(self):
        """Authenticated user without any companion should not see people in the list"""
        success_status_code = 200
        self.client.force_login(self.user_without_companion)

        response = self.client.get(self.person_list_url)

        # User should be able to access the people list
        self.assertEqual(response.status_code, success_status_code)

        # People list should not contain any existing people
        self.assertNotContains(response, self.person_with_companion_name)
        self.assertNotContains(response, self.person_without_companion_name)

    def test_authenticated_user_with_companion(self):
        """Authenticated user should be able to see person to whom they are a companion"""
        success_status_code = 200
        self.client.force_login(self.user_with_companion)

        response = self.client.get(self.person_list_url)

        # User should be able to access the people list
        self.assertEqual(response.status_code, success_status_code)

        # People list should not contain any existing people
        self.assertContains(response, self.person_with_companion_name)
        self.assertNotContains(response, self.person_without_companion_name)
