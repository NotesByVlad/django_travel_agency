import datetime
from decimal import Decimal
import pytest
from travel.services.trip_services import (
    calculate_trip_duration,
    calculate_adult_price,
    calculate_child_price
)

@pytest.mark.django_db
def test_calculate_trip_duration():
    departure_date = datetime.date(2025, 6, 1)
    return_date = datetime.date(2025, 6, 10)
    assert calculate_trip_duration(departure_date, return_date) == 9

@pytest.mark.django_db
def test_calculate_adult_price():
    hotel_price_per_day = Decimal('100.00')
    profit_on_adult = Decimal('0.10')
    departure_date = datetime.date(2025, 6, 1)
    return_date = datetime.date(2025, 6, 6)  # 5 days
    quantity = 2

    price = calculate_adult_price(hotel_price_per_day, profit_on_adult, departure_date, return_date, quantity)

    base_price = hotel_price_per_day * 5
    expected_price = (base_price + base_price * profit_on_adult) * quantity

    assert price == expected_price

@pytest.mark.django_db
def test_calculate_child_price():
    hotel_price_per_day = Decimal('80.00')
    profit_on_child = Decimal('0.05')
    departure_date = datetime.date(2025, 7, 10)
    return_date = datetime.date(2025, 7, 15)  # 5 days
    quantity = 1

    price = calculate_child_price(hotel_price_per_day, profit_on_child, departure_date, return_date, quantity)

    base_price = hotel_price_per_day * 5
    expected_price = base_price + (base_price * profit_on_child)

    assert price == expected_price