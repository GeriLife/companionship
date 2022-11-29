from circles.models import Circle
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View

from .forms import ActivityModelForm
from .models import Activity


class ActivityCreateView(UserPassesTestMixin, LoginRequiredMixin, View):
    raise_exception = True

    def test_func(self, *args, **kwargs):
        """
        Only circle's care organizers and companions can add a care group activity.
        """
        circle_id = self.request.POST.get("circle", None)

        if circle_id:
            circle = Circle.objects.get(id=circle_id)

            user_is_organizer = self.request.user in circle.organizers
            user_is_companion = self.request.user in circle.companions

            user_can_update_activity = user_is_organizer or user_is_companion

            return user_can_update_activity
        else:
            return False

    def post(self, *args, **kwargs):
        form = ActivityModelForm(self.request.POST)

        if form.is_valid():
            activity = form.save()

            redirect_to = reverse(
                "circle-detail",
                kwargs={
                    "pk": activity.circle.id,
                },
            )

            return HttpResponseRedirect(redirect_to)


class ActivityUpdateView(UserPassesTestMixin, LoginRequiredMixin, View):
    raise_exception = True

    def test_func(self, *args, **kwargs):
        """Only circle's care organizers and companions can update activity"""

        circle_id = self.request.POST.get("circle", None)

        if circle_id:
            circle = Circle.objects.get(id=circle_id)

            user_is_organizer = self.request.user in circle.organizers
            user_is_companion = self.request.user in circle.companions

            user_can_update_activity = user_is_organizer or user_is_companion

            return user_can_update_activity
        else:
            pass

    def post(self, *args, **kwargs):
        activity = Activity.objects.get(pk=kwargs["pk"])
        form = ActivityModelForm(
            self.request.POST,
            instance=activity,
        )

        if form.is_valid():
            activity = form.save()

            redirect_to = reverse(
                "circle-detail",
                kwargs={
                    "pk": activity.circle.id,
                },
            )

            return HttpResponseRedirect(redirect_to)


class ActivityDeleteView(UserPassesTestMixin, LoginRequiredMixin, View):
    raise_exception = True

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


class ActivityAddParticipantView(UserPassesTestMixin, LoginRequiredMixin, View):
    raise_exception = True

    def test_func(self, *args, **kwargs):
        """
        Only the circle's care organizers can add other companions to activity.
        Only the circle's companions can add themselves to an activity.
        """

        activity_id = self.kwargs.get("activity_id", None)

        if activity_id:
            activity = Activity.objects.get(id=activity_id)

            user_is_organizer = self.request.user in activity.circle.organizers
            user_is_companion = self.request.user in activity.circle.companions

            user_id = self.request.POST.get("user_id", None)
            user_is_adding_self = user_id == str(self.request.user.id)

            user_can_add_participant = user_is_organizer or (
                user_is_companion and user_is_adding_self
            )

            return user_can_add_participant

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


class ActivityRemoveParticipantView(UserPassesTestMixin, LoginRequiredMixin, View):
    raise_exception = True

    def test_func(self, *args, **kwargs):
        """
        Only the circle's care organizers can remove other companions from activity.
        Only the circle's companions can remove themselves from an activity.
        Non-companions or anonymous users should not be able to remove themselves,
        although they wouldn't be added in the first place.
        """
        activity_id = self.kwargs.get("activity_id", None)

        if activity_id:
            activity = Activity.objects.get(id=activity_id)

            user_is_not_companion = self.request.user not in activity.circle.companions

            if user_is_not_companion:
                return False

            user_is_organizer = self.request.user in activity.circle.organizers

            user_id = self.request.POST.get("user_id", None)
            user_is_removing_self = user_id == str(self.request.user.id)

            user_can_remove_participant = user_is_organizer or user_is_removing_self

            return user_can_remove_participant

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


class ActivitySetDoneView(UserPassesTestMixin, LoginRequiredMixin, View):
    raise_exception = True

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
