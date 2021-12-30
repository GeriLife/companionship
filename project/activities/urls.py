from django.urls import path

from .views import (
    ActivityCreateView,
    ActivityUpdateView,
)

urlpatterns = [
    path(
        "create",
        ActivityCreateView.as_view(),
        name="activity-create",
    ),
    path(
        "update",
        ActivityUpdateView.as_view(),
        name="activity-create",
    ),
]
