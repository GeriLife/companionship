from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

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


# First, ensure user is logged in, then make sure they pass test (are a companion)
class PersonDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Person
    context_object_name = "person"
    template_name = "people/person_detail.html"

    def test_func(self, *args, **kwargs):
        """Only companions (and organizers) can access the person detail view"""
        person = Person.objects.get(id=self.kwargs["pk"])
        user = self.request.user

        # Check whether user is person's companion
        user_can_access_person = user in person.companions

        return user_can_access_person

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


class PersonListView(LoginRequiredMixin, TemplateView):
    template_name = "people/person_list.html"


# First, ensure user is logged in, then make sure they pass test (are an organizer)
class PersonUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Person
    fields = [
        "name",
        "photo",
    ]

    def test_func(self, *args, **kwargs):
        """Only organizers can update the person's details"""
        person = Person.objects.get(id=self.kwargs["pk"])
        user = self.request.user

        # Check whether user is person's care organizer
        user_can_update_person = user in person.organizers

        return user_can_update_person

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


class JoinRequestUpdateView(View):
    def get(self, request, person_id, join_request_id, *args, **kwargs):
        person = Person.objects.get(id=person_id)

        # Only organizer can update join requests
        if not request.user in person.organizers:
            raise PermissionDenied()
        else:
            join_request = JoinRequest.objects.get(id=join_request_id, person=person)

            join_request_status = request.GET["status"]

            # If approved, add join request user as companion to person
            if join_request_status == "APPROVED":
                companion = Companion(
                    person=person,
                    user=join_request.user,
                )
                companion.save()

            # Always delete the join request once it has been handled by the organizer
            join_request.delete()

            return redirect(person)
