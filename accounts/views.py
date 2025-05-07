from .forms import CustomUserCreationForm
from .models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
from travel.models import Booking
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from travel.services.airport_services import calculate_plane_ticket_cost
from .services import get_user_booking_context

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

        # Call the service function to get the booking data
        booking_context_data = get_user_booking_context(user)

        # Update the context with the data from the service function
        context.update(booking_context_data)

        return context


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user = self.object

    #     bookings = Booking.objects.filter(user=user, paid=False)
    #     for booking in bookings:
    #         price_for_tickets = (
    #             booking.trip.calculate_adult_price(booking.tickets_adult) +
    #             booking.trip.calculate_child_price(booking.tickets_child)
    #         )
    #         booking.price_for_tickets = price_for_tickets

    #     paid_bookings = Booking.objects.filter(user=user, paid=True)
    #     for booking in paid_bookings:
            
    #         # Calculate the individual and total prices for this paid booking
    #         adult_price = booking.trip.calculate_adult_price(booking.tickets_adult)
    #         child_price = booking.trip.calculate_child_price(booking.tickets_child)
    #         total_price = adult_price + child_price

    #         # Attach the calculated values to the paid booking object
    #         booking.adult_price = adult_price
    #         booking.child_price = child_price
    #         booking.total_price = total_price

    #         if booking.from_airport:
    #             from_country = booking.from_airport.city.country
    #             from_continent = booking.from_airport.city.country.continent
    #             to_country = booking.trip.airport.city.country
    #             to_continent = booking.trip.airport.city.country.continent
    #             plane_tickets_cost = calculate_plane_ticket_cost(
    #                                         booking.from_airport.standard_plane_ticket, 
    #                                         from_country, from_continent, 
    #                                         to_country, to_continent)
    #             booking.plane_tickets_cost = plane_tickets_cost * booking.total_tickets()
    #             booking.airport_pickup_total = booking.trip.airport.airport_pick_up_cost * booking.total_tickets()
    #             booking.airport_dropoff_total = booking.trip.airport.airport_drop_off_cost * booking.total_tickets()

    #     context['bookings'] = bookings
    #     context['paid_bookings'] = paid_bookings

    #     return context
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
