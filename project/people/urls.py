from django.urls import path

from .views import (
    PersonCreateView,
    PersonDetailView,
    PersonListView,
    PersonUpdateView,
    join_as_companion,
)

urlpatterns = [
    path("", PersonListView.as_view(), name="person-list"),
    path(
        "create",
        PersonCreateView.as_view(),
        name="person-create",
    ),
    path("<slug:pk>/update/", PersonUpdateView.as_view(), name="person-update"),
    path("<slug:person_id>/join/", join_as_companion, name="person-join"),
    path("<slug:pk>/", PersonDetailView.as_view(), name="person-detail"),
]
