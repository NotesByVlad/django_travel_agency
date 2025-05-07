from django.shortcuts import render
from django.views.generic import DetailView, View
from travel.models import Trip
from travel.forms import TripSearchForm
from datetime import date, timedelta
from decimal import Decimal
from logging import getLogger
LOGGER = getLogger
from django.core.paginator import Paginator
from travel.services.airport_services import calculate_plane_ticket_cost

class TripInfoView(DetailView):
    model = Trip
    template_name = 'trips/trip_info.html'
    context_object_name = 'trip'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hotel = self.object.hotel

        context['images'] = hotel.images.all()
        context['stars'] = range(hotel.stars)
        return context

########################################################################

class TripSearchView(View):
    def get(self, request):
        form = TripSearchForm(request.GET or None)
        trips = Trip.objects.filter(available=True)

        # Default values BEFORE checking if form is valid
        tickets_adults = 1
        tickets_children = 0
        wants_flight = 'no'
        from_airport = None
        budget = None
        continent = country = city = departure_date = return_date = None

        if form.is_valid():
            continent = form.cleaned_data.get('continent')
            country = form.cleaned_data.get('country')
            city = form.cleaned_data.get('city')
            departure_date = form.cleaned_data.get('departure_date')
            return_date = form.cleaned_data.get('return_date')
            budget = form.cleaned_data.get('budget')

            tickets_adults = form.cleaned_data.get('tickets_adults') or 1
            tickets_children = form.cleaned_data.get('tickets_children') or 0

            wants_flight = form.cleaned_data.get('wants_flight')
            from_airport = form.cleaned_data.get('from_airport')

            # Filters
            if continent:
                trips = trips.filter(hotel__city__country__continent=continent)

            if country:
                trips = trips.filter(hotel__city__country=country)

            if city:
                trips = trips.filter(hotel__city=city)

            if departure_date and departure_date >= date.today() + timedelta(days=1):
                trips = trips.filter(departure_date__gte=departure_date)


            if departure_date and return_date:
                if return_date >= departure_date:
                    trips = trips.filter(return_date__lte=return_date)
                else:
                    # Optional: Add a message for user or ignore return_date filter
                    return render(request, 'trip_search.html', {
                        'form': form,
                        'trips': [],
                        'error': 'Return date must be after or equal to departure date.'
                    })

            if tickets_adults:
                total_requested_tickets = tickets_adults + (tickets_children or 0)
                trips = trips.filter(tickets__gte=total_requested_tickets)


            if wants_flight == 'yes' and not from_airport and budget:
                return render(request, 'trip_search.html', {
                    'form': form,
                    'trips': [],
                    'error': 'Please select a departure airport to calculate accurate flight costs for your budget.'
                })
        filtered_trips = []

        for trip in trips:
            try:
                adult_price = trip.calculate_adult_price(tickets_adults)
                child_price = trip.calculate_child_price(tickets_children)

                total_price = adult_price + child_price

                total_flight_cost = 0
                if wants_flight == 'yes' and from_airport and trip.airport:
                    flight_cost = Decimal(calculate_plane_ticket_cost(
                    trip.airport.standard_plane_ticket,
                    from_country=from_airport.city.country,
                    from_continent=from_airport.city.country.continent,
                    to_country=trip.hotel.city.country,
                    to_continent=trip.hotel.city.country.continent,
                    ))

                    total_flight_cost = flight_cost * (tickets_adults + tickets_children)
                    total_price += total_flight_cost

                if not budget or total_price <= budget:
                    trip.adult_price = adult_price
                    trip.child_price = child_price
                    trip.total_flight_cost = total_flight_cost
                    trip.total_price = total_price
                    filtered_trips.append(trip)

            except Exception as e:
                print("Error with trip:", trip, "| Error:", e)
                continue  # skip trip if any calculation fails

        paginator = Paginator(filtered_trips, 10)  # Show 10 trips per page
        page_number = request.GET.get('search_page')
        page_obj = paginator.get_page(page_number)    

        return render(request, 'trips/trip_search.html', {
            'form': form,
            'trips': page_obj,
            'tickets_adults': tickets_adults,
            'tickets_children': tickets_children,
            'budget': budget,
        })