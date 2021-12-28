from django.contrib import admin

from .models import Activity


@admin.register(Activity)
class ActivityModelAdmin(admin.ModelAdmin):
    pass
