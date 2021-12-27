from django.urls import path

from .views import CareGroupDetailView

urlpatterns = [
    path('<slug:pk>/', CareGroupDetailView.as_view(), name='care-group-detail'),
]
