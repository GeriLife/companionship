from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("User must have an email address")
        
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

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), blank=True, unique=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def get_activity_count(self, care_group=None):
        if care_group:
            activity_count = self.activities.filter(
                care_group=care_group
            ).count
        else:
            activity_count = self.activities.count

        return activity_count

    @property
    def care_groups(self):
        """
        Alias "care_groups" property since splitting out membership into "coordinating" and "participating"
        TODO: remove alias if consolidating care group membership
        """
        return self.care_groups_participating.all()