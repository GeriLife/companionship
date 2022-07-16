from django.db import models


class Caregiver(models.Model):
    class CaregiverType(models.TextChoices):
        INDIVIDUAL = "INDIVIDUAL", "Individual"
        ORGANIZATION = "ORGANIZATION", "Organization"

    display_name = models.CharField(max_length=255)
    type = models.CharField(
        max_length=15, choices=CaregiverType.choices, default=CaregiverType.INDIVIDUAL
    )

    def __str__(self):
        return f"{ self.type } - { self.display_name }"
