from django.urls import path
from .views import SignUpView, user_profile

urlpatterns = [
    path('profile/', user_profile, name='user-profile'),
    path('signup/', SignUpView.as_view(), name='signup'),
]