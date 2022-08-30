from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic.edit import CreateView, FormView

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


class UserProfileUpdateView(FormView):
    form_class = UpdateUserForm
    template_name = "accounts/profile.html"
    success_url = reverse_lazy("user-profile")

    def get_initial(self):
        initial = super().get_initial()
        initial["display_name"] = self.request.user.display_name
        initial["email"] = self.request.user.email
        return initial

    def form_valid(self, form):
        get_user_model().objects.filter(id=self.request.user.id).update(
            **form.cleaned_data
        )
        return super().form_valid(form)
