from django.contrib import admin

from .models import Companion, Person


class CompanionInline(admin.StackedInline):
    model = Companion

    extra = 0


@admin.register(Person)
class PersonModelAdmin(admin.ModelAdmin):
    inlines = [
        CompanionInline,
    ]


@admin.register(JoinRequest)
class JoinRequestAdmin(admin.ModelAdmin):
    pass
