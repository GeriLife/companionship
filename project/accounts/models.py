from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    
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