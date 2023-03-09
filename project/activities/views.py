from circles.models import Circle
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View

from .forms import ActivityModelForm
from .models import Activity
from .serializers import ActivitySerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET', 'POST'])
def activity_list(request):
    """
    Circle member(s) can create a Circle Activity via a POST request
    Circle members and coordinators can view all Circle Activities via a GET request    
    """

    circle_id = Activity.objects.values_list("circle_id", flat=True).first()
    circle = Circle.objects.get(id=circle_id)

    if request.user in circle.companions:

        if request.method == 'GET':
            activities = Activity.objects.all()
            serializer = ActivitySerializer(activities, many=True)
            return Response(serializer.data)

        if request.method == 'POST':
            serializer = ActivitySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['GET', 'PUT', 'DELETE'])
def activity_details(request, id):
    """
    Circle member(s) can update a single Circle Activity via a PUT request
    Circle coordinator(s) can delete a single Circle Activity via a DELETE request
    Circle members and coordinators can view a single Circle Activity via a GET request
    """


    try:
        activity = Activity.objects.get(pk=id)
    except Activity.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    circle_id = Activity.objects.values_list("circle_id", flat=True).get(pk=id)
    circle = Circle.objects.get(id=circle_id)

    if request.user in circle.companions:

        if request.method == 'GET':
            serializer = ActivitySerializer(activity)
            return Response(serializer.data)

        if request.method == 'PUT':
            serializer = ActivitySerializer(activity, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)  
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            if request.user in circle.organizers:
                activity.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_403_FORBIDDEN)

    return Response(status=status.HTTP_403_FORBIDDEN)

        
class ActivityCreateView(UserPassesTestMixin, LoginRequiredMixin, View):
    raise_exception = True

    def test_func(self, *args, **kwargs):
        """
        Only circle's care organizers and companions can add a care group activity.
        """
        circle_id = self.request.POST.get("circle", None)

        if circle_id:
            circle = Circle.objects.get(id=circle_id)

            user_is_organizer = self.request.user in circle.organizers
            user_is_companion = self.request.user in circle.companions

            user_can_update_activity = user_is_organizer or user_is_companion

            return user_can_update_activity
        return False

    def post(self, *args, **kwargs):
        form = ActivityModelForm(self.request.POST)

        if form.is_valid():
            activity = form.save()

            redirect_to = reverse(
                "circle-detail",
                kwargs={
                    "pk": activity.circle.id,
                },
            )

            return HttpResponseRedirect(redirect_to)


class ActivityUpdateView(UserPassesTestMixin, LoginRequiredMixin, View):
    raise_exception = True

    def test_func(self, *args, **kwargs):
        """Only circle's care organizers and companions can update activity"""

        circle_id = self.request.POST.get("circle", None)

        if circle_id:
            circle = Circle.objects.get(id=circle_id)

            user_is_organizer = self.request.user in circle.organizers
            user_is_companion = self.request.user in circle.companions

            user_can_update_activity = user_is_organizer or user_is_companion

            return user_can_update_activity
        return False

    def post(self, *args, **kwargs):
        activity = Activity.objects.get(pk=kwargs["pk"])
        form = ActivityModelForm(
            self.request.POST,
            instance=activity,
        )

        if form.is_valid():
            activity = form.save()

            redirect_to = reverse(
                "circle-detail",
                kwargs={
                    "pk": activity.circle.id,
                },
            )

            return HttpResponseRedirect(redirect_to)


class ActivityDeleteView(UserPassesTestMixin, LoginRequiredMixin, View):
    raise_exception = True

    def test_func(self, *args, **kwargs):
        """Only the circle's care organizers can delete activity"""
        self.activity = Activity.objects.get(id=self.kwargs["activity_id"])

        user_is_organizer = self.request.user in self.activity.circle.organizers

        user_can_delete_activity = user_is_organizer

        return user_can_delete_activity

    def post(self, request, *args, **kwargs):
        circle_id = self.activity.circle.id
        self.activity.delete()

        return redirect(
            reverse(
                "circle-detail",
                kwargs={"pk": circle_id},
            )
        )


class ActivityAddParticipantView(UserPassesTestMixin, LoginRequiredMixin, View):
    raise_exception = True

    def test_func(self, *args, **kwargs):
        """
        Only the circle's care organizers can add other companions to activity.
        Only the circle's companions can add themselves to an activity.
        """

        activity_id = self.kwargs.get("activity_id", None)

        if activity_id:
            activity = Activity.objects.get(id=activity_id)

            user_is_organizer = self.request.user in activity.circle.organizers
            user_is_companion = self.request.user in activity.circle.companions

            user_id = self.request.POST.get("user_id", None)
            user_is_adding_self = user_id == str(self.request.user.id)

            user_can_add_participant = user_is_organizer or (
                user_is_companion and user_is_adding_self
            )

            return user_can_add_participant

    def post(self, request, activity_id, *args, **kwargs):
        user_id = request.POST["user_id"]
        activity = Activity.objects.get(id=activity_id)

        activity.participants.add(user_id)

        return redirect(
            reverse(
                "circle-detail",
                kwargs={"pk": activity.circle.id},
            )
        )


class ActivityRemoveParticipantView(UserPassesTestMixin, LoginRequiredMixin, View):
    raise_exception = True

    def test_func(self, *args, **kwargs):
        """
        Only the circle's care organizers can remove other companions from activity.
        Only the circle's companions can remove themselves from an activity.
        Non-companions or anonymous users should not be able to remove themselves,
        although they wouldn't be added in the first place.
        """
        activity_id = self.kwargs.get("activity_id", None)

        if activity_id:
            activity = Activity.objects.get(id=activity_id)

            user_is_not_companion = self.request.user not in activity.circle.companions

            if user_is_not_companion:
                return False

            user_is_organizer = self.request.user in activity.circle.organizers

            user_id = self.request.POST.get("user_id", None)
            user_is_removing_self = user_id == str(self.request.user.id)

            user_can_remove_participant = user_is_organizer or user_is_removing_self

            return user_can_remove_participant

    def post(self, request, activity_id, *args, **kwargs):
        user_id = request.POST["user_id"]
        activity = Activity.objects.get(id=activity_id)

        activity.participants.remove(user_id)

        return redirect(
            reverse(
                "circle-detail",
                kwargs={"pk": activity.circle.id},
            )
        )


class ActivitySetDoneView(UserPassesTestMixin, LoginRequiredMixin, View):
    raise_exception = True

    def test_func(self, *args, **kwargs):
        """Only activity participants or circle's care organizers can update activity"""
        self.activity = Activity.objects.get(id=self.kwargs["activity_id"])

        user_is_participant = self.request.user in self.activity.participants.all()
        user_is_organizer = self.request.user in self.activity.circle.organizers

        user_can_update_activity = user_is_participant or user_is_organizer

        return user_can_update_activity

    def get(self, request, activity_id, *args, **kwargs):
        """If user passes permission tests, set activity as done."""

        self.activity.done = True

        self.activity.save()

        return redirect(
            reverse(
                "circle-detail",
                kwargs={"pk": self.activity.circle.id},
            )
        )
