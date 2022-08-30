from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, View

from .models import Activity


class ActivityCreateView(CreateView):
    model = Activity
    fields = [
        "person",
        "activity_type",
        "activity_date",
        "note",
    ]

    def get_success_url(self):
        return reverse("person-detail", kwargs={"pk": self.object.person.id})


class ActivityUpdateView(UpdateView):
    model = Activity
    fields = [
        "person",
        "activity_type",
        "activity_date",
        "note",
    ]

    def get_success_url(self):
        return reverse(
            "person-detail",
            kwargs={"pk": self.object.person.id},
        )


class ActivityAddParticipantView(View):
    def post(self, request, activity_id, *args, **kwargs):
        user_id = request.POST["user_id"]
        activity = Activity.objects.get(id=activity_id)

        activity.participants.add(user_id)

        return redirect(
            reverse(
                "person-detail",
                kwargs={"pk": activity.person.id},
            )
        )


class ActivityRemoveParticipantView(View):
    def post(self, request, activity_id, *args, **kwargs):
        user_id = request.POST["user_id"]
        activity = Activity.objects.get(id=activity_id)

        activity.participants.remove(user_id)

        return redirect(
            reverse(
                "person-detail",
                kwargs={"pk": activity.person.id},
            )
        )


class ActivitySetDoneView(UserPassesTestMixin, View):
    def test_func(self, *args, **kwargs):
        """Only activity participants or Person's care organizers can update activity"""
        self.activity = Activity.objects.get(id=self.kwargs["activity_id"])

        user_is_participant = self.request.user in self.activity.participants.all()
        user_is_organizer = self.request.user in self.activity.person.organizers

        user_can_update_activity = user_is_participant or user_is_organizer

        return user_can_update_activity

    def get(self, request, activity_id, *args, **kwargs):
        """If user passes permission tests, set activity as done."""

        self.activity.done = True

        self.activity.save()

        return redirect(
            reverse(
                "person-detail",
                kwargs={"pk": self.activity.person.id},
            )
        )
