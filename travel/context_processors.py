from travel.models import Country, Continent, City
from .forms import TripSearchForm
import json

def trip_search_form(request):
    # Get all countries and their corresponding continents
    countries_json = json.dumps([
        {'id': country.id, 'name': country.name, 'continent_id': country.continent.id}
        for country in Country.objects.all()
    ])

    # Get all continents
    continents_json = json.dumps([
        {'id': continent.id, 'name': continent.name}
        for continent in Continent.objects.all()
    ])

    # Get all cities and their corresponding countries and continents
    cities_json = json.dumps([
        {'id': city.id, 'name': city.name, 'country_id': city.country.id, 'continent_id': city.country.continent.id}
        for city in City.objects.all()
    ])

    return {
        'trip_search_form': TripSearchForm(),
        'countries_json': countries_json,
        'continents_json': continents_json,
        'cities_json': cities_json,
    }