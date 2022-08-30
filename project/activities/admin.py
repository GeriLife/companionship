from django.contrib import admin

from .models import Activity


@admin.register(Activity)
class ActivityModelAdmin(admin.ModelAdmin):
    fields = [
        "activity_type",
        "activity_date",
        "person",
    ]
