from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from activities.forms import ActivitModelForm

from .models import CareGroup


class CareGroupCreateView(LoginRequiredMixin, CreateView):
    model = CareGroup
    fields = ["name"]


class CareGroupDetailView(LoginRequiredMixin, DetailView):
    model = CareGroup
    context_object_name = "group"
    template_name = "care_groups/caregroup_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["add_activity_form"] = ActivitModelForm

        return context


class CareGroupListView(LoginRequiredMixin, ListView):
    model = CareGroup
    context_object_name = "groups"


class CareGroupUpdateView(LoginRequiredMixin, UpdateView):
    model = CareGroup
    fields = ["name"]
