from django.urls import include, path
from rest_framework import routers

from .views import (
    ActivityAddParticipantView,
    ActivityCreateView,
    ActivityDeleteView,
    ActivityRemoveParticipantView,
    ActivitySetDoneView,
    ActivityUpdateView,
    ActivityViewSet,
)

router = routers.SimpleRouter()
router.register(r"activities", ActivityViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "create",
        ActivityCreateView.as_view(),
        name="activity-create",
    ),
    path(
        "delete/<slug:activity_id>/",
        ActivityDeleteView.as_view(),
        name="activity-delete",
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
    path(
        "update/<slug:activity_id>/set_done",
        ActivitySetDoneView.as_view(),
        name="activity-set-done",
    ),
]
