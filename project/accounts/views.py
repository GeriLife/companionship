from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from dj_rest_auth.registration.views import VerifyEmailView

from .forms import CustomUserCreationForm, UpdateUserForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("circle-list")
    template_name = "registration/signup.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        next = self.request.GET.get("next")

        if next:
            context["next"] = next

        return context

    def form_valid(self, form):
        """If the form is valid, save the associated model and log the user in."""
        user = form.save()

        # Ensure the user is logged in
        login(self.request, user)

        next = self.request.POST.get("next")

        # Allow specifying the next URL when signing up
        if next is not None:
            return redirect(next)
        return redirect(self.success_url)


class UserProfileUpdateView(UpdateView):
    form_class = UpdateUserForm
    template_name = "accounts/profile.html"
    success_url = reverse_lazy("user-profile")

    def get_object(self):
        return self.request.user


class ApiVerifyEmailView(VerifyEmailView):
    template_name = "accounts/email_verified.html"
