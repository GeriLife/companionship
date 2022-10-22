from django.urls import path

from .views import (
    CircleCreateView,
    CircleDetailView,
    CircleListView,
    CircleUpdateView,
    CompanionDeleteView,
    JoinRequestUpdateView,
    join_as_companion,
)

urlpatterns = [
    path("", CircleListView.as_view(), name="circle-list"),
    path(
        "create",
        CircleCreateView.as_view(),
        name="circle-create",
    ),
    path("<slug:pk>/update/", CircleUpdateView.as_view(), name="circle-update"),
    path("<slug:circle_id>/join/", join_as_companion, name="circle-join"),
    path("<slug:pk>/", CircleDetailView.as_view(), name="circle-detail"),
    path(
        "<slug:circle_id>/join-request/<slug:join_request_id>",
        JoinRequestUpdateView.as_view(),
        name="update-join-request",
    ),
    path(
        "<slug:circle_id>/companion/<pk>/delete",
        CompanionDeleteView.as_view(),
        name="delete-companion",
    ),
]
