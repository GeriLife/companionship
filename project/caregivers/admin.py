from django.contrib import admin

from .models import Caregiver


@admin.register(Caregiver)
class CaregiverModelAdmin(admin.ModelAdmin):
    pass
