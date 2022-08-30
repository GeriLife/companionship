from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic.edit import CreateView, UpdateView

from .forms import CustomUserCreationForm, UpdateUserForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("home")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        """If the form is valid, save the associated model and log the user in."""
        user = form.save()

        login(self.request, user)

        return redirect(self.success_url)


class UserProfileUpdateView(UpdateView):
    form_class = UpdateUserForm
    template_name = "accounts/profile.html"
    success_url = reverse_lazy("user-profile")

    def get_object(self):
        return self.request.user
