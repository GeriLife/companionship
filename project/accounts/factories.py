import random

from factory.django import DjangoModelFactory
from faker import Faker

from .models import User

fake = Faker()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = fake.email()
    display_name = fake.name()
    is_staff = bool(random.getrandbits(1))
    is_active = bool(random.getrandbits(1))
