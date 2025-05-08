from django.urls import path
from django.contrib.auth.views import LogoutView
from accounts.views import CustomLoginView, RegisterView

urlpatterns = [
    path('login/', CustomLoginView.as_view(template_name='accounts/auth/login_register.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]
