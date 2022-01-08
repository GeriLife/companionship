from datetime import datetime
import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.fields import CharField
from django.utils.translation import gettext as _
from django.urls import reverse

User = get_user_model()


class CareGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = _("care group")
        verbose_name_plural = _("care groups")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("care-group-detail", kwargs={"pk": self.pk})

    @property
    def upcoming_activities(self):
        today = datetime.today()

        return self.activities.filter(activity_date__gte=today)

    @property
    def annotated_members(self):
        """
        Return a member list annotated with activity count for current group.

        TODO: refactor for performance,
            such as by defining a specific CareGroupMember model with "activity_count" property that can be cached.
            This will also provide a unified list of coordinators and members.
        """
        annotated_members = []

        for member in self.members.all():
            member.activity_count = member.get_activity_count(care_group=self)

            annotated_members.append(member)

        return annotated_members

    @property
    def companionship_score(self):
        """
        Companionship score is the number of times people have participated in care group activities.
        E.g., if a care group has ten activities and each activity has had two participants, the companionship score will be 20.

        Thanks goes to Marcel from StackOverflow
        https://stackoverflow.com/a/70592240/1191545
        """

        return User.objects.filter(activities__care_group=self).count()


class CareGroupMembership(models.Model):
    care_group = models.ForeignKey(
        to=CareGroup, related_name="memberships", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        to=User, related_name="care_group_memberships", on_delete=models.CASCADE
    )
    is_organizer = models.BooleanField(default=False)

    def __str__(self):
        return self.user.display_name

    def get_activity_count(self, care_group=None):
        return self.user.get_activity_count(care_group=self.care_group)
