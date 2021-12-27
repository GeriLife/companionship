from django.urls import path

from .views import CareGroupDetailView, CareGroupListView

urlpatterns = [
    path('', CareGroupListView.as_view(), name='care-group-list'),
    path('<slug:pk>/', CareGroupDetailView.as_view(), name='care-group-detail'),
]
