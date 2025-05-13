from django.test import TestCase
from travel.models import Continent, Country, City, Hotel, Airport

class CountryTestCase(TestCase):
    def setUp(self):
        self.continent = Continent.objects.create(name="Europe")
# 1.
    def test_country_continent_relation(self):
        country = Country.objects.create(name="France", continent=self.continent)
        self.assertEqual(country.continent.name, "Europe")

class CityTestCase(TestCase):
    def setUp(self):
        self.continent = Continent.objects.create(name='Europe')
        self.country = Country.objects.create(name="France", continent=self.continent)
        self.city = City.objects.create(name="Paris", country=self.country, car_rental_option=True, car_rental_cost=50)
# 2.   
    def test_city_car_rental(self):
        self.assertTrue(self.city.car_rental_option)
        self.assertEqual(self.city.car_rental_cost, 50)

class HotelTestCase(TestCase):
    def setUp(self):
        self.continent = Continent.objects.create(name='Europe')
        self.country = Country.objects.create(name="France", continent=self.continent)
        self.city = City.objects.create(name="Paris", country=self.country, car_rental_option=True)
   
# 3.
    def test_hotel_price_per_day(self):
        hotel = Hotel.objects.create(
            name="Hotel Paris", city=self.city, price_per_day=100, capacity=50, stars=5)
        self.assertEqual(hotel.price_per_day, 100)
# 4.
    def test_hotel_meal_plans(self):
        hotel = Hotel.objects.create(
                name="Hotel Paris", city=self.city, price_per_day=100, 
                bb_price=20, hb_price=30.0, fb_price=40.0, ai_price=50,
                capacity=50, stars=5)
        self.assertEqual(hotel.bb_price, 20)

class AirportTestCase(TestCase):
    def setUp(self):
        self.continent = Continent.objects.create(name='Europe')
        self.country = Country.objects.create(name="France", continent=self.continent)
        self.city = City.objects.create(name="Paris", country=self.country, car_rental_option=True)
   
# 5.
    def test_airport_ticket_price(self):
        airport = Airport.objects.create(name="CDG", code="CDG", city=self.city, standard_plane_ticket=150)
        self.assertEqual(airport.standard_plane_ticket, 150)
# 6.
    def test_airport_pick_up_cost(self):
        airport = Airport.objects.create(name="CDG", code="CDG", city=self.city, airport_pick_up_cost=20)
        self.assertEqual(airport.airport_pick_up_cost, 20)
# 7.
    def test_airport_drop_off_cost(self):
        airport = Airport.objects.create(name="CDG", code="CDG", city=self.city, airport_pick_up_cost=20)
        self.assertEqual(airport.airport_pick_up_cost, 20)