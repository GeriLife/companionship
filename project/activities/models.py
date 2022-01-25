import datetime
from enum import Enum

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from people.models import Person

User = get_user_model()

class Activity(models.Model):
    class ActivityTypeIcons(Enum):
        APPOINTMENT = "bi-calendar-event"
        CALL = "bi-camera-video"
        ENTERTAINMENT = "bi-ticket-perforated"
        ERRAND = "bi-building"
        HOUSEWORK = "bi-house"
        NATURE = "bi-tree"
        OUTING = "bi-cup-straw"
        SHOPPING = "bi-cart"

    class ActivityTypeChoices(models.TextChoices):
        APPOINTMENT = "APPOINTMENT", _("Appointment")
        CALL = "CALL", _("Call")
        ENTERTAINMENT = "ENTERTAINMENT", _("Entertainment")
        ERRAND = "ERRAND", _("Errand")
        HOUSEWORK = "HOUSEWORK", _("Housework")
        NATURE = "NATURE", _("Nature")
        OUTING = "OUTING", _("Outing")
        SHOPPING = "SHOPPING", _("Shopping")

    activity_type = models.CharField(
        max_length=15,
        choices=ActivityTypeChoices.choices,
        default=ActivityTypeChoices.APPOINTMENT,
    )

    activity_date = models.DateField(default=datetime.date.today)

    note = models.CharField(
        max_length=50,
        help_text=_("Optionally, add a brief note. For privacy, avoid adding sensitive information."),
        null=True,
        blank=True,
    )

    person = models.ForeignKey(
        to=Person,
        related_name="activities",
        on_delete=models.CASCADE,
        null=True,
    )

    participants = models.ManyToManyField(User, related_name="activities")

    class Meta:
        verbose_name = _("activity")
        verbose_name_plural = _("activities")
        ordering = ["activity_date",]

    def __str__(self):
        return self.get_activity_type_display()

    def get_absolute_url(self):
        return reverse("activity-detail", kwargs={"pk": self.pk})

    @property
    def icon(self):
        return self.ActivityTypeIcons[self.activity_type].value

    @property
    def remaining_person_companions(self):
        # Only care group members are eligible to participate
        companions = User.objects.filter(companions__person=self.person)

        # Get current activity participants
        current_participants = self.participants.all()

        # Exclude existing participants from care group members
        return companions.difference(current_participants)
