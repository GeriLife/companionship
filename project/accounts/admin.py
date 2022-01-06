from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = [
        "email",
        "display_name",
    ]
    ordering = [
        "email",
        "display_name",
    ]
    list_filter = [
        "is_staff",
        "is_superuser",
    ]
    fieldsets = (
        (
            "Details",
            {
                "fields": ("email", "display_name", "password"),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "display_name",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    search_fields = ("email", "display_name")
