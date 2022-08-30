from django.urls import path

from .views import SignUpView, UserProfileUpdateView

urlpatterns = [
    path("profile/", UserProfileUpdateView.as_view(), name="user-profile"),
    path("signup/", SignUpView.as_view(), name="signup"),
]
