from django.db import models
from django.urls import reverse
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

    activity_date = models.DateField(auto_now=True,)

    class Meta:
        verbose_name = _("activity")
        verbose_name_plural = _("activities")

    def __str__(self):
        return self.get_activity_type_display()

    def get_absolute_url(self):
        return reverse("care-group-detail", kwargs={"pk": self.pk})
