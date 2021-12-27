from django.views.generic.detail import DetailView

from .models import CareGroup


class CareGroupDetailView(DetailView):
    model = CareGroup
    context_object_name = "group"
