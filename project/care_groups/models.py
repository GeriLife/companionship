import uuid
from django.db import models
from django.db.models.fields import CharField
from django.utils.translation import gettext as _
from django.urls import reverse

from accounts.models import User


class CareGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    members = models.ManyToManyField(User, related_name="care_groups",)

    class Meta:
        verbose_name = _("care group")
        verbose_name_plural = _("care groups")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("care-group-detail", kwargs={"pk": self.pk})
