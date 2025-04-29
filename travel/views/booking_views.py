from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from travel.models import Trip, Booking, Invoice, Airport
from travel.forms import BookingForm
from logging import getLogger
LOGGER = getLogger
import logging
# Booking CRUD ########################################


##################################################################################


class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.trip = get_object_or_404(Trip, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        return {'trip': self.trip}

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.trip = self.trip
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print("Form is invalid!")
        logging.error(f"Form is invalid! Errors: {form.errors}")
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trip'] = self.trip
        context['user'] = self.request.user

        ## Passing context to template - then -> javascript for dynamic price display
        context['trip_duration'] = self.trip.calculate_duration()

        # 1. For tickets
        context['adult_unit_price'] = self.trip.calculate_adult_price()
        context['child_unit_price'] = self.trip.calculate_child_price()

        # 2. For meal plans
        hotel = self.trip.hotel
        context['meal_plan_prices'] = {'None': 0,
                                        'BB': hotel.bb_price or 0,
                                        'HB': hotel.hb_price or 0,
                                        'FB': hotel.fb_price or 0,
                                        'AI': hotel.ai_price or 0}

        # 3. For car rental
        city = self.trip.city
        context['city_car_rental_cost'] = city.car_rental_cost if city.car_rental_cost else 0

        # 4. For airport services
        # 4.1 For plane tickets
        all_airports = Airport.objects.all()

        # Get destination info
        to_country = self.trip.city.country
        to_continent = to_country.continent

        airport_data = {}
        for airport in all_airports:
            airport_data[airport.id] = {
                'country': airport.city.country.name,
                'continent': airport.city.country.continent.name,
                'standard_ticket': airport.standard_plane_ticket
            }

        context['airport_data'] = airport_data
        context['to_country'] = to_country.name
        context['to_continent'] = to_continent.name

        # 4.2 For airport pickup and dropoff
        airport = self.trip.airport
        context['airport_pickup_cost'] = airport.airport_pick_up_cost or 0
        context['airport_dropoff_cost'] = airport.airport_drop_off_cost or 0

        return context

    def get_success_url(self):
        return reverse_lazy('user_profile', kwargs={'username': self.request.user.username})


##################################################################################


class BookingUpdateView(UpdateView):
    template_name = 'bookings/booking_form.html'
    form_class = BookingForm
    model = Booking
    success_url = reverse_lazy('booking_success')

    def dispatch(self, request, *args, **kwargs):
        # Retrieve the Booking object based on the pk from the URL
        self.booking = self.get_object()  # Retrieves the Booking object based on the URL
        self.trip = self.booking.trip      # Get the associated Trip object
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Custom form validation to ensure the number of tickets does not exceed available tickets
        trip = self.trip  # Use the trip associated with the booking
        total_tickets = form.instance.tickets_adult + form.instance.tickets_child

        if total_tickets > trip.tickets:
            form.add_error(None, f"Only {trip.tickets} tickets are available for this trip.")
            return self.form_invalid(form)

        # Additional custom logic here if needed
        return super().form_valid(form)

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Reuse the logic from BookingCreateView's get_context_data
        context['trip'] = self.trip
        context['user'] = self.request.user

        # Assuming that the trip object doesn’t change during booking update.
        context['trip_duration'] = self.trip.calculate_duration()

        # Tickets prices
        context['adult_unit_price'] = self.trip.calculate_adult_price()
        context['child_unit_price'] = self.trip.calculate_child_price()

        # Meal plans
        hotel = self.trip.hotel
        context['meal_plan_prices'] = {'None': 0,
                                        'BB': hotel.bb_price or 0,
                                        'HB': hotel.hb_price or 0,
                                        'FB': hotel.fb_price or 0,
                                        'AI': hotel.ai_price or 0}

        # Car rental
        city = self.trip.city
        context['city_car_rental_cost'] = city.car_rental_cost if city.car_rental_cost else 0

        # Airport services
        all_airports = Airport.objects.all()
        to_country = self.trip.city.country
        to_continent = to_country.continent

        airport_data = {}
        for airport in all_airports:
            airport_data[airport.id] = {
                'country': airport.city.country.name,
                'continent': airport.city.country.continent.name,
                'standard_ticket': airport.standard_plane_ticket
            }

        context['airport_data'] = airport_data
        context['to_country'] = to_country.name
        context['to_continent'] = to_continent.name

        # Airport pickup and dropoff costs
        airport = self.trip.airport
        context['airport_pickup_cost'] = airport.airport_pick_up_cost or 0
        context['airport_dropoff_cost'] = airport.airport_drop_off_cost or 0

        return context


##################################################################################

    
class BookingDeleteView(LoginRequiredMixin, DeleteView):
    model = Booking
    template_name = 'bookings/booking_confirm_delete.html'
    success_url = reverse_lazy('booking_success') 

    def get_object(self, queryset=None):
        booking = get_object_or_404(Booking, pk=self.kwargs.get('pk'))
        return booking

    def form_valid(self, form):
        self.object = self.get_object()
        return super().form_valid(form)
    

##################################################################################


class PayBookingView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        booking = get_object_or_404(Booking, pk=kwargs['pk'], user=request.user)

        if not hasattr(booking, 'invoice'):
            Invoice.objects.create(booking=booking)

        return redirect('user_profile', username=request.user.username)
    



##################################################################################



def booking_success(request):
    # If you're storing the last trip in session or redirect args:
    trip_pk = request.session.get('last_trip_id')  # or get from GET params
    trip = Trip.objects.get(pk=trip_pk) if trip_pk else None

    return render(request, 'bookings/booking_success.html', {'trip': trip})