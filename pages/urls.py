from django.urls import path
from .views import HomeView
from travel.views.contact_views import ContactFormView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contact/', ContactFormView.as_view(), name='contact')
]