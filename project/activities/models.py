from django.db import models
from django.utils.translation import gettext_lazy as _


class Activity(models.Model):
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
