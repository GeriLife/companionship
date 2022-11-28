from factory import fuzzy
from factory.django import DjangoModelFactory
from faker import Faker

from .models import Caregiver

fake = Faker()


class CaregiverFactory(DjangoModelFactory):
    class Meta:
        model = Caregiver

    display_name = fake.first_name()
    type = fuzzy.FuzzyChoice(Caregiver.CaregiverType)
