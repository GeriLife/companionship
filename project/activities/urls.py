from django.urls import path

from .views import (
    ActivityCreateView,
    ActivityUpdateView,
    ActivityAddParticipantView,
)

urlpatterns = [
    path(
        "create",
        ActivityCreateView.as_view(),
        name="activity-create",
    ),
    path(
        "update/<slug:pk>/",
        ActivityUpdateView.as_view(),
        name="activity-update",
    ),
    path(
        "update/<slug:activity_id>/add_participant",
        ActivityAddParticipantView.as_view(),
        name="activity-add-participant",
    ),
]
