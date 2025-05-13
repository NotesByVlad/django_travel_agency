from django.urls import path
from accounts.views import UserProfileView, EditProfileView

urlpatterns = [
    path('profile/<str:username>/', UserProfileView.as_view(), name='user_profile'),
    path('profile/<str:username>/edit/', EditProfileView.as_view(), name='edit_profile'),
]
