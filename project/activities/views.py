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