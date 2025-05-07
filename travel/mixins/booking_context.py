from django.shortcuts import get_object_or_404
from ..models import Airport


class BookingContextMixin:
    def get_booking_context(self, trip):
        context = {}
        context['trip'] = trip
        context['user'] = self.request.user
        context['trip_duration'] = trip.calculate_duration()

        # Tickets prices
        context['adult_unit_price'] = trip.calculate_adult_price()
        context['child_unit_price'] = trip.calculate_child_price()

        # Meal plans
        hotel = trip.hotel
        context['meal_plan_prices'] = {
            'None': 0,
            'BB': hotel.bb_price or 0,
            'HB': hotel.hb_price or 0,
            'FB': hotel.fb_price or 0,
            'AI': hotel.ai_price or 0
        }

        # Car rental
        city = trip.city
        context['city_car_rental_cost'] = city.car_rental_cost if city.car_rental_cost else 0

        # Airport services
        all_airports = Airport.objects.all()
        to_country = trip.city.country
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

        # Airport pickup/dropoff costs
        airport = trip.airport
        context['airport_pickup_cost'] = airport.airport_pick_up_cost or 0
        context['airport_dropoff_cost'] = airport.airport_drop_off_cost or 0

        return context