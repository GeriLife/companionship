from django.contrib import admin

from .models import Companion, JoinRequest, Circle


class CompanionInline(admin.StackedInline):
    model = Companion

    extra = 0


@admin.register(Circle)
class CircleModelAdmin(admin.ModelAdmin):
    inlines = [
        CompanionInline,
    ]


@admin.register(JoinRequest)
class JoinRequestAdmin(admin.ModelAdmin):
    pass
