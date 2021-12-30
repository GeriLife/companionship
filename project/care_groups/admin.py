from django.contrib import admin

from .models import CareGroup


@admin.register(CareGroup)
class CareGroupModelAdmin(admin.ModelAdmin):
    pass
