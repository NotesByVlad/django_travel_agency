from django.urls import path
from accounts.views import ActivateAccountView

urlpatterns = [
    path('activate/<uid>/<token>/', ActivateAccountView.as_view(), name='activate'),
]
