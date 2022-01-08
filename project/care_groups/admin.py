from django.contrib import admin

from .models import CareGroup, CareGroupMembership


class CareGroupMemberInline(admin.StackedInline):
    model = CareGroupMembership

    extra = 0


@admin.register(CareGroup)
class CareGroupModelAdmin(admin.ModelAdmin):
    inlines = [
        CareGroupMemberInline,
    ]
