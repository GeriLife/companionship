from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "display_name")
        widgets = {
            "email": forms.TextInput(attrs={"placeholder": "your@email.com"}),
            "display_name": forms.TextInput(attrs={"placeholder": _("Display name")}),
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        # Clear the default value for display name
        self.fields["display_name"].initial = None


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "display_name")


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["display_name", "email"]
