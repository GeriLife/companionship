from datetime import datetime
import uuid
from django.db import models
from django.db.models.fields import CharField
from django.utils.translation import gettext as _
from django.urls import reverse

from accounts.models import User


class CareGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    # TODO: refactor members to use single model
    # with properties for "is_coordinator" and "activity_count" (which can be cached)
    members = models.ManyToManyField(
        User,
        related_name="care_groups_participating",
    )
    coordinators = models.ManyToManyField(User, related_name="care_groups_coordinating")

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

        for coordinator in self.coordinators.all():
            coordinator.is_coordinator = True

            coordinator.activity_count = coordinator.get_activity_count(care_group=self)

            annotated_members.append(coordinator)


        for member in self.members.difference(self.coordinators.all()):
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
