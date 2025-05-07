from travel.models import Trip, Continent, Country
from django.utils import timezone
from django.views.generic import ListView
from datetime import timedelta

class HomeView(ListView):
    template_name = 'index.html'
    context_object_name = 'trips_promoted'

    def get_tomorrow(self):
        return timezone.now() + timedelta(days=1)

    def get_queryset(self):
        tomorrow = self.get_tomorrow()
        return Trip.objects.filter(
            promoted=True,
            available=True,
            departure_date__gt=tomorrow
        ).order_by('departure_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tomorrow = self.get_tomorrow()

        base_queryset = Trip.objects.filter(
            available=True,
            departure_date__gt=tomorrow
        )

        # Read selected continent or country
        selected_continent_id = self.request.GET.get('continent_id')
        selected_country_id = self.request.GET.get('country_id')

        # Build trips for continent carousel
        trips_for_continent_carousel = base_queryset
        if selected_continent_id:
            trips_for_continent_carousel = trips_for_continent_carousel.filter(
                city__country__continent__pk=selected_continent_id
            )

        # Build trips for country carousel
        trips_for_country_carousel = base_queryset
        if selected_country_id:
            trips_for_country_carousel = trips_for_country_carousel.filter(
                city__country__pk=selected_country_id
            )

        # Trips
        trips_promoted = base_queryset.filter(promoted=True).order_by('departure_date')
        trips_global = base_queryset.order_by('departure_date')

        # All trips grouped by continent
        trips_by_continent = {
            continent: base_queryset.filter(city__country__continent=continent).order_by('departure_date')
            for continent in Continent.objects.all()
        }

        # All trips grouped by country
        trips_by_country = {
            country: base_queryset.filter(city__country=country).order_by('departure_date')
            for country in Country.objects.all()
        }

        # Build context
        context.update({
            'trips_promoted': trips_promoted,
            'trips_global': trips_global,
            'trips_for_continent_carousel': trips_for_continent_carousel.order_by('departure_date'),
            'trips_for_country_carousel': trips_for_country_carousel.order_by('departure_date'),
            'trips_continent': trips_by_continent,
            'trips_country': trips_by_country,
            'selected_continent_id': selected_continent_id,
            'selected_country_id': selected_country_id,
        })

        return context