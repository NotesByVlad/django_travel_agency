from django.core.exceptions import ValidationError
from django.utils import timezone
from django.test import TestCase
from datetime import timedelta
from travel.models import Continent, Country, City, Airport, Hotel, Trip
from unittest.mock import patch
from decimal import Decimal

class TripModelTests(TestCase):
    def setUp(self):
        self.continent = Continent.objects.create(name='Europe')
        self.country = Country.objects.create(name='France', continent=self.continent)
        self.city = City.objects.create(name='Paris', country=self.country, car_rental_option=False)
        self.hotel = Hotel.objects.create(name='Paris Hotel', city=self.city, capacity=100, price_per_day=100,
                                          stars=5)
# 1.
    def test_calculate_duration(self):
        trip = Trip(
            hotel=self.hotel,
            departure_date=timezone.now().date(),
            return_date=timezone.now().date() + timedelta(days=5)
        )
        self.assertEqual(trip.calculate_duration(), 5)
# 2.
    @patch('travel.services.trip_services.calculate_adult_price')
    def test_calculate_adult_price(self, mocked_service):
        trip = Trip(
            hotel=self.hotel,
            departure_date=timezone.now().date(),
            return_date=timezone.now().date() + timedelta(days=5),
            profit_on_adult=0.2
        )   # (5 days * 100$price/day) + (5 days * 2$profit) = 510
        mocked_service.return_value = 600.00
        self.assertAlmostEqual(trip.calculate_adult_price(), Decimal('600.00'))
# 3.
    @patch('travel.services.trip_services.calculate_child_price')
    def test_calculate_child_price(self, mocked_service):
        trip = Trip(
            hotel=self.hotel,
            departure_date=timezone.now().date(),
            return_date=timezone.now().date() + timedelta(days=5),
            profit_on_child=0.1
        )  # (5 days * 100$price/day) + (5 days * 1$profit) = 505
        mocked_service.return_value = 550.00
        self.assertAlmostEqual(trip.calculate_child_price(), Decimal('550.00'))
# 4.
    def test_clean_dates_return_before_departure(self):
        trip = Trip(
            hotel=self.hotel,
            departure_date=timezone.now().date() + timedelta(days=1),
            return_date=timezone.now().date()
        )
        with self.assertRaises(ValidationError):
            trip.clean_dates()
# 5.
    def test_clean_capacity_overlap(self):
        existing_trip = Trip.objects.create(
            hotel=self.hotel,
            departure_date=timezone.now().date() + timedelta(days=1),
            return_date=timezone.now().date() + timedelta(days=5),
            tickets=100 # top capacity of hotel
        )
        overlapping_trip = Trip(
            hotel=self.hotel,
            departure_date=existing_trip.departure_date,
            return_date=existing_trip.return_date,
            tickets=3  # over capacity with 3
        )
        with self.assertRaises(ValidationError):
            overlapping_trip.clean_capacity_overlap()


#     def test_clean_locations(self):
#         hotel = Hotel.objects.first()
#         trip = Trip(
#             hotel=hotel,
#             departure_date=timezone.now().date() + timedelta(days=1),
#             return_date=timezone.now().date() + timedelta(days=5)
#         )
#         trip.clean_locations()
#         self.assertEqual(trip.city, hotel.city)
#         self.assertEqual(trip.airport, hotel.city.airports.first())


# class TripModelTests(TestCase):
#     def test_clean_tickets_exceed_capacity(self):
#         hotel = Hotel.objects.first()
#         trip = Trip(
#             hotel=hotel,
#             departure_date=timezone.now().date() + timedelta(days=1),
#             return_date=timezone.now().date() + timedelta(days=5),
#             tickets=hotel.capacity + 1  # Invalid: exceeds capacity
#         )
#         with self.assertRaises(ValidationError):
#             trip.clean_tickets()


# class TripModelTests(TestCase):
#     def test_clean_dates_return_before_departure(self):
#         trip = Trip(
#             hotel=Hotel.objects.first(),
#             departure_date=timezone.now().date() + timedelta(days=1),
#             return_date=timezone.now().date()  # Invalid: return date before departure date
#         )
#         with self.assertRaises(ValidationError):
#             trip.clean_dates()

#     def test_clean_dates_departure_in_the_past(self):
#         trip = Trip(
#             hotel=Hotel.objects.first(),
#             departure_date=timezone.now().date() - timedelta(days=1),  # Invalid: departure in the past
#             return_date=timezone.now().date() + timedelta(days=1)
#         )
#         with self.assertRaises(ValidationError):
#             trip.clean_dates()