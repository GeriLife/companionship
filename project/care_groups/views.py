from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import CareGroup


class CareGroupDetailView(DetailView):
    model = CareGroup
    context_object_name = "group"

class CareGroupListView(ListView):
    model = CareGroup
    context_object_name = "groups"