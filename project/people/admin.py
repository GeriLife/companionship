from django.contrib import admin

from .models import Person, Companion


class CompanionInline(admin.StackedInline):
    model = Companion

    extra = 0


@admin.register(Person)
class PersonModelAdmin(admin.ModelAdmin):
    inlines = [
        CompanionInline,
    ]
