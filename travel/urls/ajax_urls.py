from django.urls import path
from travel.views.ajax_views import LoadCitiesView

app_name = 'travel_ajax'

urlpatterns = [
    path('load-cities/', LoadCitiesView.as_view(), name='load_cities'),
]