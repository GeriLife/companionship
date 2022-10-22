from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, View

from .models import Activity


class ActivityCreateView(CreateView):
    model = Activity
    fields = [
        "circle",
        "activity_type",
        "activity_date",
        "note",
    ]

    def get_success_url(self):
        return reverse("circle-detail", kwargs={"pk": self.object.circle.id})


class ActivityUpdateView(UpdateView):
    model = Activity
    fields = [
        "circle",
        "activity_type",
        "activity_date",
        "note",
    ]

    def get_success_url(self):
        return reverse(
            "circle-detail",
            kwargs={"pk": self.object.circle.id},
        )


class ActivityDeleteView(UserPassesTestMixin, View):
    def test_func(self, *args, **kwargs):
        """Only the circle's care organizers can delete activity"""
        self.activity = Activity.objects.get(id=self.kwargs["activity_id"])

        user_is_organizer = self.request.user in self.activity.circle.organizers

        user_can_delete_activity = user_is_organizer

        return user_can_delete_activity

    def post(self, request, *args, **kwargs):
        circle_id = self.activity.circle.id
        self.activity.delete()

        return redirect(
            reverse(
                "circle-detail",
                kwargs={"pk": circle_id},
            )
        )


class ActivityAddParticipantView(View):
    def post(self, request, activity_id, *args, **kwargs):
        user_id = request.POST["user_id"]
        activity = Activity.objects.get(id=activity_id)

        activity.participants.add(user_id)

        return redirect(
            reverse(
                "circle-detail",
                kwargs={"pk": activity.circle.id},
            )
        )


class ActivityRemoveParticipantView(View):
    def post(self, request, activity_id, *args, **kwargs):
        user_id = request.POST["user_id"]
        activity = Activity.objects.get(id=activity_id)

        activity.participants.remove(user_id)

        return redirect(
            reverse(
                "circle-detail",
                kwargs={"pk": activity.circle.id},
            )
        )


class ActivitySetDoneView(UserPassesTestMixin, View):
    def test_func(self, *args, **kwargs):
        """Only activity participants or circle's care organizers can update activity"""
        self.activity = Activity.objects.get(id=self.kwargs["activity_id"])

        user_is_participant = self.request.user in self.activity.participants.all()
        user_is_organizer = self.request.user in self.activity.circle.organizers

        user_can_update_activity = user_is_participant or user_is_organizer

        return user_can_update_activity

    def get(self, request, activity_id, *args, **kwargs):
        """If user passes permission tests, set activity as done."""

        self.activity.done = True

        self.activity.save()

        return redirect(
            reverse(
                "circle-detail",
                kwargs={"pk": self.activity.circle.id},
            )
        )
