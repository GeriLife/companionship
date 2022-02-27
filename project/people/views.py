from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from activities.forms import ActivityModelForm

from .models import JoinRequest, Person, Companion


class PersonCreateView(LoginRequiredMixin, CreateView):
    model = Person
    fields = [
        "name",
        "photo",
    ]

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

        """
        {{ request.get_host }}{% url 'person-join' person.id %}
        """

        # Create companion invitation URL
        person_id = context["person"].id
        invitation_path = reverse("person-join", kwargs={"person_id": person_id})
        invitation_url = self.request.build_absolute_uri(invitation_path)

        context["invitation_url"] = invitation_url

        context["add_activity_form"] = ActivityModelForm

        return context


class PersonListView(LoginRequiredMixin, ListView):
    model = Person
    context_object_name = "people"


class PersonUpdateView(LoginRequiredMixin, UpdateView):
    model = Person
    fields = [
        "name",
        "photo",
    ]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.fields["name"].widget.attrs.update({"autofocus": "autofocus"})

        return form


@login_required
def join_as_companion(request, person_id):
    try:
        person = Person.objects.get(pk=person_id)
    except Person.DoesNotExist:
        message = _("Could not find person at the requested URL")
        raise Http404(message)

    # Redirect to person page if user is already a companion
    if Companion.objects.filter(
        person=person_id,
        user=request.user,
    ).exists():
        return redirect(person)

    # Show "request received" if user has already submitted a join request
    if JoinRequest.objects.filter(
        person=person_id,
        user=request.user,
    ).exists():
        return render(request, "people/person_join_received.html")

    # Handle join request
    if request.method == "POST":
        join_request = JoinRequest(
            person=person,
            user=request.user,
        )

        join_request.save()

        return render(request, "people/person_join_received.html")

    # Show join form by default
    return render(request, "people/person_join.html")
