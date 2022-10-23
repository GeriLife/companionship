from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError(_("User must have an email address"))

        email = self.normalize_email(email)
        user = self.model(email=email)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create a new user with superuser permissions"""
        user = self.create_user(email, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class User(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(_("email address"), unique=True)
    display_name = models.CharField(
        _("display name"),
        max_length=15,
        help_text=_(
            "Helps other team members recognise you, such as by your given name or nickname."  # noqa: E501
        ),
        default="Given name",
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(default=True)

    @property
    def is_care_circle_organizer(self):
        user_is_care_circle_organizer = self.companions_through.filter(
            is_organizer=True,
        ).exists()

        return user_is_care_circle_organizer

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_activity_count(self, circle=None):
        if circle:
            activity_count = self.activities.filter(circle=circle).count
        else:
            activity_count = self.activities.count

        return activity_count
