import random

import factory
from accounts.factories import UserFactory
from factory.django import DjangoModelFactory
from faker import Faker

from .models import Circle, Companion

fake = Faker()


class CircleFactory(DjangoModelFactory):
    class Meta:
        model = Circle

    name = fake.word()


class CompanionFactory(DjangoModelFactory):
    class Meta:
        model = Companion

    circle = factory.SubFactory(CircleFactory)
    user = factory.SubFactory(UserFactory)
    is_organizer = bool(random.getrandbits(1))
