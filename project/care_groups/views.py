from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from .models import CareGroup


class CareGroupCreateView(CreateView):
    model = CareGroup
    fields = ["name"]


class CareGroupDetailView(DetailView):
    model = CareGroup
    context_object_name = "group"


class CareGroupListView(ListView):
    model = CareGroup
    context_object_name = "groups"


class CareGroupUpdateView(UpdateView):
    model = CareGroup
    fields = ["name"]
