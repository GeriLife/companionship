from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from activities.forms import ActivityModelForm

from .models import Person, Companion


class PersonCreateView(LoginRequiredMixin, CreateView):
    model = Person
    fields = ["name", "photo",]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.fields["name"].widget.attrs.update({"autofocus": "autofocus"})

        return form

    def form_valid(self, form):
        # Save person
        # so we can add request user as coordinator
        person = form.save()

        # Add user who creates a person as organizer
        companion = Companion(
            person=person,
            user=self.request.user,
            is_organizer=True,
        )

        companion.save()

        return HttpResponseRedirect(person.get_absolute_url())


class PersonDetailView(LoginRequiredMixin, DetailView):
    model = Person
    context_object_name = "person"
    template_name = "people/person_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["add_activity_form"] = ActivityModelForm

        return context


class PersonListView(LoginRequiredMixin, ListView):
    model = Person
    context_object_name = "people"


class PersonUpdateView(LoginRequiredMixin, UpdateView):
    model = Person
    fields = ["name", "photo",]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.fields["name"].widget.attrs.update({"autofocus": "autofocus"})

        return form
