from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from .models import CareGroup


@admin.register(CareGroup)
class CareGroupModelAdmin(admin.ModelAdmin):
    pass
