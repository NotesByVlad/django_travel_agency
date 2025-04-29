from .forms import CustomUserCreationForm
from .models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
from travel.models import Booking, Trip
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

class UserProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'profile.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def dispatch(self, request, *args, **kwargs):
        # Get the user object based on the username in the URL
        user = self.get_object()
        
        # If the logged-in user is not the profile owner, redirect them
        if user != request.user:
            return redirect('home')  # Or redirect to any other page
        
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object

        context['bookings'] = Booking.objects.filter(user=user)
        context['promoted'] = Trip.objects.filter(promoted=True)

        return context

class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'accounts_form.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_type'] = 'register'
        # Add the login form instance to the context
        context['register_form'] = AuthenticationForm()  # Include login form in the context
        return context


class CustomLoginView(LoginView):
    template_name = 'accounts_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_type'] = 'login'
        # Add the registration form instance to the context
        context['login_form'] = CustomUserCreationForm()  # Include registration form in the context
        return context
