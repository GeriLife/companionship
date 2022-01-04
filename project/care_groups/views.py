from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from activities.forms import ActivityModelForm

from .models import CareGroup


class CareGroupCreateView(LoginRequiredMixin, CreateView):
    model = CareGroup
    fields = ["name"]

    def form_valid(self, form):
        # Save care group 
        # so we can add request user as coordinator
        care_group = form.save()

        # Add user who creates a care group as coordinator
        care_group.coordinators.add(self.request.user)

        care_group.save()

        return HttpResponseRedirect(care_group.get_absolute_url())


class CareGroupDetailView(LoginRequiredMixin, DetailView):
    model = CareGroup
    context_object_name = "group"
    template_name = "care_groups/caregroup_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["add_activity_form"] = ActivityModelForm

        return context


class CareGroupListView(LoginRequiredMixin, ListView):
    model = CareGroup
    context_object_name = "groups"


class CareGroupUpdateView(LoginRequiredMixin, UpdateView):
    model = CareGroup
    fields = ["name"]
