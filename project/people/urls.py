from django.urls import path

from .views import (
    PersonCreateView,
    PersonDetailView,
    PersonListView,
    PersonUpdateView,
)

urlpatterns = [
    path("", PersonListView.as_view(), name="person-list"),
    path(
        "create",
        PersonCreateView.as_view(),
        name="person-create",
    ),
    path("update/<slug:pk>/", PersonUpdateView.as_view(), name="person-update"),
    path("<slug:pk>/", PersonDetailView.as_view(), name="person-detail"),
]
