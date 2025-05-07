from travel.models import Booking
from travel.services.airport_services import calculate_plane_ticket_cost

def get_user_booking_context(user):
    """
    Fetches user bookings and calculates price details for context.
    """
    context_data = {}
    # Logic for unpaid bookings
    bookings = Booking.objects.filter(user=user, paid=False)
    for booking in bookings:
        price_for_tickets = (
            booking.trip.calculate_adult_price(booking.tickets_adult) +
            booking.trip.calculate_child_price(booking.tickets_child)
        )
        booking.price_for_tickets = price_for_tickets # Attach to booking object

    context_data['bookings'] = bookings

    # Logic for paid bookings
    paid_bookings = Booking.objects.filter(user=user, paid=True)
    for booking in paid_bookings:
        # Calculate the individual and total prices for this paid booking
        adult_price = booking.trip.calculate_adult_price(booking.tickets_adult)
        child_price = booking.trip.calculate_child_price(booking.tickets_child)
        total_price = adult_price + child_price

        # Attach the calculated values to the paid booking object
        booking.adult_price = adult_price
        booking.child_price = child_price
        booking.total_price = total_price

        if booking.from_airport and booking.trip.airport: # Add check for trip.airport
            from_country = booking.from_airport.city.country
            from_continent = booking.from_airport.city.country.continent
            to_country = booking.trip.airport.city.country
            to_continent = booking.trip.airport.city.country.continent

            try:
                plane_tickets_cost = calculate_plane_ticket_cost(
                                            booking.from_airport.standard_plane_ticket,
                                            from_country, from_continent,
                                            to_country, to_continent)
                booking.plane_tickets_cost = plane_tickets_cost * booking.total_tickets()
            except Exception as e:
                print(f"Error calculating plane ticket cost for booking {booking.id}: {e}")
                booking.plane_tickets_cost = 0

            booking.airport_pickup_total = booking.trip.airport.airport_pick_up_cost * booking.total_tickets()
            booking.airport_dropoff_total = booking.trip.airport.airport_drop_off_cost * booking.total_tickets()
        else:
             booking.plane_tickets_cost = 0
             booking.airport_pickup_total = 0
             booking.airport_dropoff_total = 0

    context_data['paid_bookings'] = paid_bookings

    return context_data