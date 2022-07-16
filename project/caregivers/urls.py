from django.urls import path

from .views import CaregiverListView


urlpatterns = [
    path(
        "",
        CaregiverListView.as_view(),
        name="caregiver-list-view",
    )
]
