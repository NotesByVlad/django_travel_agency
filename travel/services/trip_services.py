from decimal import Decimal

def calculate_trip_duration(departure_date, return_date):
    return (return_date - departure_date).days

def calculate_adult_price(hotel_price_per_day, profit_on_adult, departure_date, return_date, quantity=1):
    duration = calculate_trip_duration(departure_date, return_date)
    base_price = hotel_price_per_day * duration
    adult_price = base_price + (base_price * Decimal(profit_on_adult))
    return adult_price * quantity

def calculate_child_price(hotel_price_per_day, profit_on_child, departure_date, return_date, quantity=1):
    duration = calculate_trip_duration(departure_date, return_date)
    base_price = hotel_price_per_day * duration
    child_price = base_price + (base_price * Decimal(profit_on_child))
    return child_price * quantity