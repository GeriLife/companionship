from django.db import models

from django_countries.fields import CountryField


class Caregiver(models.Model):
    class CaregiverType(models.TextChoices):
        INDIVIDUAL = "INDIVIDUAL", "Individual"
        ORGANIZATION = "ORGANIZATION", "Organization"

    display_name = models.CharField(max_length=255)
    type = models.CharField(
        max_length=15, choices=CaregiverType.choices, default=CaregiverType.INDIVIDUAL
    )


class CaregiverLocality(models.Model):
    """Represents the locality  (i.e. city) where a caregiver provides service."""

    country = CountryField()
    region = models.CharField(
        max_length=255,
        help_text="The region in which the locality is, and which is in the country. For example, California or another appropriate first-level Administrative division",
    )
    locality = models.CharField(
        max_length=255,
        help_text="The locality in which the street address is, and which is in the region. For example, Mountain View.",
    )
