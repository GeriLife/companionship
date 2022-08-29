from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "display_name")
        widgets = {
            "email": forms.TextInput(attrs={"placeholder": "person@domain.com"}),
            "display_name": forms.TextInput(attrs={"placeholder": "Display name"}),
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
