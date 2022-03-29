from datetime import datetime
import uuid

from easy_thumbnails.fields import ThumbnailerImageField

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.fields import CharField
from django.utils.translation import gettext as _
from django.urls import reverse

User = get_user_model()


class Person(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    photo = ThumbnailerImageField(upload_to="people_photos", blank=True)

    class Meta:
        verbose_name_plural = _("people")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("person-detail", kwargs={"pk": self.pk})

    @property
    def organizers(self):
        organizers = User.objects.filter(companions__person=self, companions__is_organizer=True)

        return organizers

    @property
    def upcoming_activities(self):
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

        for member in self.companions.all():
            member.activity_count = member.get_activity_count(person=self)

            annotated_companions.append(member)

        return annotated_companions

    @property
    def companionship_score(self):
        """
        Companionship score is the number of times people have participated in care group activities.
        E.g., if a care group has ten activities and each activity has had two participants, the companionship score will be 20.

        Thanks goes to Marcel from StackOverflow
        https://stackoverflow.com/a/70592240/1191545
        """

        return User.objects.filter(activities__person=self).count()

    @property
    def pending_join_requests(self):
        """Get join requests who have not been approved or rejected."""
        return self.join_requests.filter(status="PENDING")


class Companion(models.Model):
    person = models.ForeignKey(
        to=Person, related_name="companions", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        to=User, related_name="companions", on_delete=models.CASCADE
    )
    is_organizer = models.BooleanField(default=False)

    def __str__(self):
        return self.user.display_name

    def get_activity_count(self, person=None):
        return self.user.get_activity_count(person=self.person)

    class Meta:
        unique_together = ('person', 'user',)


class JoinRequest(models.Model):
    """Request to join as a personal companion."""

    class JoinRequestStatusChoices(models.TextChoices):
        PENDING = "PENDING", _("Pending")
        APPROVED = "APPROVED", _("Approved")
        REJECTED = "REJECTED", _("Rejected")

    person = models.ForeignKey(
        to=Person, related_name="join_requests", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        to=User, related_name="join_requests", on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=15,
        choices=JoinRequestStatusChoices.choices,
        default=JoinRequestStatusChoices.PENDING,
    )
