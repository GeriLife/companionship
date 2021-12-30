from django.urls import path

from .views import (
    ActivityCreateView,
    ActivityUpdateView,
    ActivityAddParticipantView,
    ActivityRemoveParticipantView,
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
    path(
        "update/<slug:activity_id>/remove_participant",
        ActivityRemoveParticipantView.as_view(),
        name="activity-remove-participant",
    ),
]
