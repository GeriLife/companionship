from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic.edit import CreateView


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


@login_required
def user_profile(request):
    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()

            messages.success(request, _("Profile updated successfully"))

            return redirect(to="user-profile")
        else:
            messages.error(request, _("Profile form isn't valid"))
    else:
        user_form = UpdateUserForm(instance=request.user)

    return render(request, "accounts/profile.html", {"user_form": user_form})
