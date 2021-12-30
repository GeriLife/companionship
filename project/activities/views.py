from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, View

from .models import Activity


class ActivityCreateView(CreateView):
    model = Activity
    fields = [
        "care_group",
        "activity_type",
        "activity_date",
    ]

    def get_success_url(self):
        return reverse("care-group-detail", kwargs={"pk": self.object.care_group.id})


class ActivityUpdateView(UpdateView):
    model = Activity
    fields = [
        "care_group",
        "activity_type",
        "activity_date",
    ]

    def get_success_url(self):
        return reverse(
            "care-group-detail",
            kwargs={"pk": self.object.care_group.id},
        )


class ActivityAddParticipantView(View):
    def post(self, request, activity_id, *args, **kwargs):
        user_id = request.POST["user_id"]
        activity = Activity.objects.get(id=activity_id)

        activity.participants.add(user_id)

        return redirect(
            reverse(
                "care-group-detail",
                kwargs={"pk": activity.care_group.id},
            )
        )


class ActivityRemoveParticipantView(View):
    def post(self, request, activity_id, *args, **kwargs):
        user_id = request.POST["user_id"]
        activity = Activity.objects.get(id=activity_id)

        activity.participants.remove(user_id)

        return redirect(
            reverse(
                "care-group-detail",
                kwargs={"pk": activity.care_group.id},
            )
        )