import factory
import random
from factory.django import DjangoModelFactory
from .models import Circle, Companion
from accounts.factories import UserFactory
from faker import Faker

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
