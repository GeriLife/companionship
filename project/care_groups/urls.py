from django.urls import path

from .views import (
    CareGroupCreateView,
    CareGroupDetailView,
    CareGroupListView,
    CareGroupUpdateView,
)

urlpatterns = [
    path("", CareGroupListView.as_view(), name="care-group-list"),
    path(
        "create",
        CareGroupCreateView.as_view(),
        name="care-group-create",
    ),
    path("update/<slug:pk>/", CareGroupUpdateView.as_view(), name="care-group-update"),
    path("<slug:pk>/", CareGroupDetailView.as_view(), name="care-group-detail"),
]
