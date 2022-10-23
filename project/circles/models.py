import uuid
from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from easy_thumbnails.fields import ThumbnailerImageField

User = get_user_model()


class Circle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    photo = ThumbnailerImageField(upload_to="circle_photos", blank=True)

    class Meta:
        verbose_name_plural = _("circles")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("circle-detail", kwargs={"pk": self.pk})

    @property
    def companions(self):
        """Return a list of users who are companions for this circle."""
        companions = User.objects.filter(companions_through__circle=self)

        return companions

    @property
    def organizers(self):
        """Return a list of users who are care organizers for this circle."""
        organizers = User.objects.filter(
            companions_through__circle=self,
            companions_through__is_organizer=True,
        )

        return organizers

    @property
    def upcoming_activities(self):
        """Return a list of activities that happen today or later."""
        today = datetime.today()

        return self.activities.filter(activity_date__gte=today)

    @property
    def annotated_companions(self):
        """
        Return a companion list annotated with activity count for current persion.

        TODO: refactor for performance,
            such as by adding a cached "activity_count" property to Companion model
        """
        annotated_companions = []

        for member in self.companions_through.all():
            member.activity_count = member.get_activity_count(circle=self)

            annotated_companions.append(member)

        return annotated_companions

    @property
    def companionship_score(self):
        """
        Companionship score is the number of times companions have
        participated in care group activities.
        E.g., if a care group has ten activities and each activity
        has had two participants, the companionship score
        will be 20.

        Thanks goes to Marcel from StackOverflow
        https://stackoverflow.com/a/70592240/1191545
        """

        return User.objects.filter(activities__circle=self).count()

    @property
    def pending_join_requests(self):
        """Get join requests who have not been approved or rejected."""
        return self.join_requests.filter(status="PENDING")


class Companion(models.Model):
    circle = models.ForeignKey(
        to=Circle, related_name="companions_through", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        to=User, related_name="companions_through", on_delete=models.CASCADE
    )
    is_organizer = models.BooleanField(default=False)

    def __str__(self):
        return self.user.display_name

    def get_activity_count(self, circle=None):
        """Return a count of activities between the related user and circle."""
        return self.user.get_activity_count(circle=self.circle)

    class Meta:
        unique_together = (
            "circle",
            "user",
        )


class JoinRequest(models.Model):
    """Request to join circle as a companion."""

    class JoinRequestStatusChoices(models.TextChoices):
        PENDING = "PENDING", _("Pending")
        APPROVED = "APPROVED", _("Approved")
        REJECTED = "REJECTED", _("Rejected")

    circle = models.ForeignKey(
        to=Circle, related_name="join_requests", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        to=User, related_name="join_requests", on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=15,
        choices=JoinRequestStatusChoices.choices,
        default=JoinRequestStatusChoices.PENDING,
    )
