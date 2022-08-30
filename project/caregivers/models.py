from django.db import models
from django.utils.translation import gettext_lazy as _


class Caregiver(models.Model):
    class CaregiverType(models.TextChoices):
        INDIVIDUAL = "INDIVIDUAL", _("Individual")
        ORGANIZATION = "ORGANIZATION", _("Organization")

    display_name = models.CharField(max_length=255)
    type = models.CharField(
        max_length=15, choices=CaregiverType.choices, default=CaregiverType.INDIVIDUAL
    )

    def __str__(self):
        return f"{ self.type } - { self.display_name }"
