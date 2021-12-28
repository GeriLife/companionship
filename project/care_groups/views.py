from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from activities.forms import ActivitModelForm
from .models import CareGroup


class CareGroupCreateView(CreateView):
    model = CareGroup
    fields = ["name"]


class CareGroupDetailView(DetailView):
    model = CareGroup
    context_object_name = "group"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["add_activity_form"] = ActivitModelForm

        return context


class CareGroupListView(ListView):
    model = CareGroup
    context_object_name = "groups"


class CareGroupUpdateView(UpdateView):
    model = CareGroup
    fields = ["name"]
