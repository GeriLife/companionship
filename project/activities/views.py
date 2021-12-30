from django.urls import reverse
from django.views.generic import CreateView, UpdateView

from .models import Activity


class ActivityCreateView(CreateView):
    model = Activity
    fields = [
        "care_group",
        "activity_type",
        "activity_date",
    ]

    def get_success_url(self):
        return reverse("care-group-detail", kwargs={"pk": self.object.care_group.id })


class ActivityUpdateView(UpdateView):
    model = Activity
    fields = [
        "care_group",
        "activity_type",
        "activity_date",
    ]

    def get_success_url(self):
        return reverse("care-group-detail", kwargs={"pk": self.object.care_group.id })
