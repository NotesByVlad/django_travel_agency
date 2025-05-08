from accounts.models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from accounts.services import get_user_booking_context

class UserProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'accounts/profile/profile.html'
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

        # Call the service function to get the booking data
        booking_context_data = get_user_booking_context(user)

        # Update the context with the data from the service function
        context.update(booking_context_data)

        return context