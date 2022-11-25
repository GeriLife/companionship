import random

from factory.django import DjangoModelFactory
from .models import User
from faker import Faker

fake = Faker()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = fake.email()
    display_name = fake.name()
    is_staff = bool(random.getrandbits(1))
    is_active = bool(random.getrandbits(1))
