from .views import UserProfileView, RegisterView, CustomLoginView
from django.contrib.auth.views import LogoutView
from django.urls import path


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(template_name='accounts_form.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/<str:username>/', UserProfileView.as_view(), name='user_profile')
]