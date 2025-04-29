from django.urls import path
from travel.views import TripInfoView, TripSearchView

urlpatterns = [
    path('trip/<int:pk>/', TripInfoView.as_view(), name='trip_info'),
    path('search/trips/', TripSearchView.as_view(), name='search_trips'),
]
