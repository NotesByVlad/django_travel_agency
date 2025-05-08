from django.urls import path
from accounts.views import UserProfileView

urlpatterns = [
    path('profile/<str:username>/', UserProfileView.as_view(), name='user_profile'),
]
