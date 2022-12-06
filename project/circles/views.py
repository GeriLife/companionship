from activities.forms import ActivityModelForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Circle, Companion, JoinRequest


class CompanionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Companion
    context_object_name = "companion"

    def get_success_url(self):
        return reverse("circle-detail", kwargs={"pk": self.object.circle.id})

    def test_func(self):
        """
        Only care organizer can remove companions for the related circle

        Also, make sure the Circle ID in the URL path matches the
        Circle ID from the Companion object.This is to encourage
        that the requesting user knows the correct Circle ID,
        since Companion PKs are sequential.
        """
        request_circle_id = self.kwargs["circle_id"]

        companion = self.get_object()

        circle = companion.circle

        user = self.request.user

        # Tests
        # TODO: determine if there is a more idiomatic way
        # to validate the request circle_id
        user_can_remove_companion = user in circle.organizers
        request_circle_id_matches_circle_id = request_circle_id == str(circle.id)

        return user_can_remove_companion and request_circle_id_matches_circle_id


class CircleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Circle
    fields = [
        "name",
        "photo",
    ]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.fields["name"].widget.attrs.update({"autofocus": "autofocus"})

        return form

    def form_valid(self, form):
        # Save circle
        # so we can add request user as coordinator
        circle = form.save()

        # Add user who creates a circle as organizer
        companion = Companion(
            circle=circle,
            user=self.request.user,
            is_organizer=True,
        )

        companion.save()

        return HttpResponseRedirect(circle.get_absolute_url())

    def test_func(self) -> bool:
        """
        For now, users can only create at most one Circle (a.k.a. care circle)

        The limit is intended to reduce the liklihood of abuse while eventually
        encouraging users to become supporters when that tier becomes available.

        Here, we check whether a user is already a care circle organizer. If so,
        they cannot add a new Circle (care circle).
        """

        return not self.request.user.is_care_circle_organizer


# First, ensure user is logged in, then make sure they pass test (are a companion)
class CircleDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Circle
    context_object_name = "circle"
    template_name = "circles/circle_detail.html"

    def test_func(self, *args, **kwargs):
        """Only companions (and organizers) can access the circle detail view"""
        circle = Circle.objects.get(id=self.kwargs["pk"])
        user = self.request.user

        # Check whether user is circle's companion
        user_can_access_circle = user in circle.companions

        return user_can_access_circle

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.object.activities.all()
        paginator = Paginator(queryset, 4)
        page = self.request.GET.get("page")

        """
        {{ request.get_host }}{% url 'circle-join' circle.id %}
        """

        # Create companion invitation URL
        circle_id = context["circle"].id
        invitation_path = reverse("circle-join", kwargs={"circle_id": circle_id})
        invitation_url = self.request.build_absolute_uri(invitation_path)

        context["invitation_url"] = invitation_url

        context["add_activity_form"] = ActivityModelForm

        try:
            activities_page = paginator.page(page)
        except PageNotAnInteger:
            activities_page = paginator.page(1)
        except EmptyPage:
            activities_page = paginator.page(paginator.num_pages)

        context["activity_page"] = activities_page

        return context


class CircleListView(LoginRequiredMixin, TemplateView):
    template_name = "circles/circle_list.html"


# First, ensure user is logged in, then make sure they pass test (are an organizer)
class CircleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Circle
    fields = [
        "name",
        "photo",
    ]

    def test_func(self, *args, **kwargs):
        """Only organizers can update the circle's details"""
        circle = Circle.objects.get(id=self.kwargs["pk"])
        user = self.request.user

        # Check whether user is circle's care organizer
        user_can_update_circle = user in circle.organizers

        return user_can_update_circle

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.fields["name"].widget.attrs.update({"autofocus": "autofocus"})

        return form

    def form_valid(self,form):
        """Used to delete old photos and thumbnails"""
        circle = Circle.objects.get(id=self.kwargs["pk"])
        circle.photo.delete()

        circle = form.save()

        return HttpResponseRedirect(circle.get_absolute_url())


def join_as_companion(request, circle_id):
    if request.user.is_authenticated:
        # Ensure circle exists
        try:
            circle = Circle.objects.get(pk=circle_id)
        except Circle.DoesNotExist:
            message = _("Could not find circle at the requested URL")
            raise Http404(message)

        # Redirect to circle page if user is already a companion
        if Companion.objects.filter(
            circle=circle_id,
            user=request.user,
        ).exists():
            return redirect(circle)

        # Show "request received" if user has already submitted a join request
        if JoinRequest.objects.filter(
            circle=circle_id,
            user=request.user,
        ).exists():
            return render(request, "circles/circle_join_received.html")

        # Handle join request
        if request.method == "POST":
            join_request = JoinRequest(
                circle=circle,
                user=request.user,
            )

            join_request.save()

            return render(request, "circles/circle_join_received.html")

        # Show join form by default
        return render(request, "circles/circle_join.html")
    else:
        # Show login/register buttons by default
        return render(request, "circles/login_register.html")


class JoinRequestUpdateView(View):
    def get(self, request, circle_id, join_request_id, *args, **kwargs):
        circle = Circle.objects.get(id=circle_id)

        # Only organizer can update join requests
        if request.user not in circle.organizers:
            raise PermissionDenied()
        else:
            join_request = JoinRequest.objects.get(id=join_request_id, circle=circle)

            join_request_status = request.GET["status"]

            # If approved, add join request user as companion to circle
            if join_request_status == "APPROVED":
                companion = Companion(
                    circle=circle,
                    user=join_request.user,
                )
                companion.save()

            # Always delete the join request once it has been handled by the organizer
            join_request.delete()

            return redirect(circle)
