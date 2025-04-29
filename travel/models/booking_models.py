from django.db import models, transaction
from .trip_models import Trip
from .location_models import Airport


from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings
from decimal import Decimal

# # # Booking Model # # #

##########################################################################
from travel.services.airport_services import calculate_plane_ticket_cost
###########################################################################

class Booking(models.Model):
    MEAL_PLAN_CHOICES = [
    ('None', 'No Meal Plan'),        # No meal plan selected
    ('BB', 'Bed and Breakfast'),     # BB: Bed and Breakfast
    ('HB', 'Half Board'),            # HB: Half Board
    ('FB', 'Full Board'),            # FB: Full Board
    ('AI', 'All Inclusive')]         # AI: All Inclusive

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(default=timezone.now)
    meal_plan = models.CharField(max_length=4, choices=MEAL_PLAN_CHOICES,default='None',
                                 help_text='Select meal plan for booking')
    tickets_adult = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)],
                                                help_text='Tickets for adults')
    tickets_child = models.PositiveIntegerField(default=0, help_text=' Tickets for children')

    wants_flight = models.BooleanField(default=False, help_text='Include flight tickets?')
    from_airport = models.ForeignKey('travel.Airport', null=True, blank=True, on_delete=models.SET_NULL,
                                     help_text='Departure Airport')
    wants_airport_pickup = models.BooleanField(default=False, help_text='Pick up from airport?')
    wants_airport_dropoff = models.BooleanField(default=False, help_text='Drop off at airport?')

    airport_price = models.IntegerField(default=0, help_text='Total cost of airport services')

    wants_car_rental = models.BooleanField(default=False, help_text='Include car rental?')
    car_rental_days = models.IntegerField(default=0, help_text='Car rental days')

    car_rental_cost = models.IntegerField(default=0, help_text='Total cost of car rental services')

    booking_price = models.IntegerField(default=0)

    paid = models.BooleanField(default=False)

    def total_tickets(self):
        return self.tickets_adult + self.tickets_child

    def calculate_meal_plan_cost(self):
        total_tickets = self.tickets_adult + self.tickets_child
        duration = self.trip.calculate_duration()

        if self.meal_plan == None:
            return 0
        
        if self.meal_plan == 'BB':
            return (self.trip.hotel.bb_price * total_tickets) * duration
        
        if self.meal_plan == 'HB':
            return (self.trip.hotel.hb_price * total_tickets) * duration
        
        if self.meal_plan == 'FB':
            return (self.trip.hotel.fb_price * total_tickets) * duration

        if self.meal_plan == 'AI':
            return (self.trip.hotel.ai_price * total_tickets) * duration

        return 0 # with no meal plan selected return 0

########################################################################


    def calculate_airport_cost(self):
        cost = 0
        to_airport = self.trip.airport # destination of trip
        from_airport = self.from_airport # selected by user


        if self.wants_flight and from_airport:

            from_country = from_airport.city.country
            from_continent = from_country.continent

            to_country = to_airport.city.country
            to_continent = to_country.continent

            # plane_ticket_cost = to_airport.calculate_plane_ticket_cost(
            #     from_country,from_continent,to_country,to_continent
            # ) 
            plane_ticket_cost = calculate_plane_ticket_cost(
                to_airport.standard_plane_ticket,
                from_country, from_continent,
                to_country, to_continent
            )

            cost += plane_ticket_cost * self.total_tickets()

            if self.wants_airport_pickup:
                cost += to_airport.airport_pick_up_cost * self.total_tickets()

            if self.wants_airport_dropoff:
                cost += to_airport.airport_drop_off_cost * self.total_tickets()

        return cost

########################################################################

    def calculate_car_rental_cost(self):
        cost = 0
        if self.wants_car_rental and self.car_rental_days != 0:
            cost_per_day = self.trip.city.car_rental_cost
            cost = cost_per_day * self.car_rental_days
            self.car_rental_cost = cost
            return cost
        return 0


########################################################################

    def total_cost(self):
        adult_ticket_price = Decimal(self.trip.calculate_adult_price(self.tickets_adult))
        child_ticket_price = Decimal(self.trip.calculate_child_price(self.tickets_child))
        # Meal plan cost
        meal_plan_cost = Decimal(self.calculate_meal_plan_cost())

        airport_cost = Decimal(self.calculate_airport_cost())  ###########
        self.airport_price = int(airport_cost)

        car_rental_cost = Decimal(self.calculate_car_rental_cost())

        self.booking_price = meal_plan_cost + adult_ticket_price + child_ticket_price + airport_cost + car_rental_cost

        return float(self.booking_price)

    def clean_tickets(self):
        booking_tickets = self.total_tickets()
        if booking_tickets > self.trip.tickets:
            raise ValidationError(f'Only {self.trip.tickets} tickets left on this trip')

    def clean_airport(self):
        if self.wants_flight and not self.from_airport:
            raise ValidationError('Flight requested, please select airport')

    def clean_car(self):
        if self.wants_car_rental and self.car_rental_days <= 0:
            raise ValidationError('Please enter valid car rental days')
        

    def clean(self):
        self.clean_tickets()
        self.clean_airport()
        self.clean_car()

    def add_tickets(self):
        booked_tickets = self.total_tickets()
        self.trip.tickets -= booked_tickets
        self.trip.save()

    def delete_tickets(self):
        booked_tickets = self.total_tickets()
        self.trip.tickets += booked_tickets
        self.trip.save()
        
    def save(self, *args, **kwargs):
        self.total_cost()

        if not self.pk:
            self.add_tickets()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.pk:
            self.delete_tickets()
        super().delete(*args, **kwargs)

    def __str__(self):
        tickets = self.total_tickets()
        trip = self.trip
        return f'{tickets} tickets for {trip}'
    



    ##### TO BE CONTINUED ###################



#   BOOKING CANNOT BE CREATED BY SAME USER IF ANOTHER BOOKING HAS SAME DATES
#   BUT CAN CREATE BOOKINGS IF DATES ARE DIFFERENT

# helper function
# get dates from trips