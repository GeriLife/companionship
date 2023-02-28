from django.urls import path

from .views import (
    ActivityAddParticipantView,
    ActivityCreateView,
    ActivityDeleteView,
    ActivityRemoveParticipantView,
    ActivitySetDoneView,
    ActivityUpdateView,
    ActivityAddCommentView,
    ActivityViewCommentView,
)

urlpatterns = [
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
    path(
        "update/<slug:activity_id>/add_comment",
        ActivityAddCommentView.as_view(),
        name="activity-add-comment",
    ),
    path(
        "<slug:activity_id>/comments",
        ActivityViewCommentView.as_view(),
        name="activity-view-comments",
    ),
]
