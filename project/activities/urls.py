from django.urls import path

from .views import (
    ActivityCreateView
)

urlpatterns = [
    path(
        "create",
        ActivityCreateView.as_view(),
        name="activity-create",
    ),
]
