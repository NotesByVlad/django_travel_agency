from django.db import models
from .location_models import City, Hotel, Airport
from django.core.exceptions import ValidationError
from django.conf import settings
import datetime
from django.utils.timezone import timedelta
from travel.services.trip_services import (
    calculate_trip_duration,
    calculate_adult_price as service_calculate_adult_price,
    calculate_child_price as service_calculate_child_price,
)


# # # Trip Model # # #
class Trip(models.Model):
    
    hotel = models.ForeignKey(Hotel, related_name='hotel_trips', on_delete=models.CASCADE, null=True, help_text='Hotel where clients make bookings')

    # City and airport are auto filled when hotel is selected with clean() method
    city = models.ForeignKey(City, related_name='city_trips', on_delete=models.CASCADE, null=True, blank=True)
    airport = models.ForeignKey(Airport, related_name='airport_trips', on_delete=models.CASCADE, null=True, blank=True)
 
    departure_date = models.DateField(help_text='When trip begins')
    return_date = models.DateField(help_text='When trip ends')

    profit_on_adult = models.DecimalField(max_digits=10, decimal_places=2, default=0.12, 
                                          help_text='example: 0.10 represent 10 % of hotel price ' \
                                          'to be added to the final cost')
    profit_on_child = models.DecimalField(max_digits=10, decimal_places=2, default=0.08,
                                          help_text='example: 0.10 represent 10 % of hotel price ' \
                                          'to be added to the final cost')

    tickets = models.PositiveIntegerField(default=1, help_text='Number of tickets including adults and children')

    promoted = models.BooleanField(default=False, help_text='Check if this trip is going to promoted section of trips')

    available = models.BooleanField(default=True, help_text='If trip is available')

    def __str__(self):
         return f' {self.calculate_duration()} days in {self.hotel.city}'
    
    def calculate_duration(self):
        return calculate_trip_duration(self.departure_date, self.return_date)
    
    def calculate_adult_price(self, quantity=1):
        return service_calculate_adult_price(
            self.hotel.price_per_day, self.profit_on_adult,
            self.departure_date, self.return_date,
            quantity)

    def calculate_child_price(self, quantity=1):
        return service_calculate_child_price(
            self.hotel.price_per_day, self.profit_on_child,
            self.departure_date, self.return_date,
            quantity)

    def has_changed(self, field_name):
        if not self.pk:
            return True
        try:
            old_value = type(self).objects.get(pk=self.pk).__dict__.get(field_name)
            new_value = getattr(self, field_name)
            return old_value != new_value
        except type(self).DoesNotExist:
            return True

    def clean_dates(self):
        # Only validate if dates are new or have changed
        if self.has_changed('departure_date') or self.has_changed('return_date'):
            if self.return_date <= self.departure_date:
                raise ValidationError('Return date must be after the departure date')

            if self.departure_date <= datetime.date.today():
                raise ValidationError('Departure date cannot be today or in the past')

    def clean_tickets(self):
        if self.tickets > self.hotel.capacity:
            raise ValidationError(f'Hotel has {self.hotel.capacity} available spots')

    def clean_locations(self):
        if not self.hotel:
            raise ValidationError('A trip must have a hotel')
        
        self.city = self.hotel.city
        self.airport = self.hotel.city.airports.first()

    def clean_capacity_overlap(self):
        #  if fields are missing the method stops early.
        if not self.hotel or not self.departure_date or not self.return_date:
            return
        
        # start from the beginning of the trip
        current_date = self.departure_date

        # Loop through each day of the trip
        while current_date <= self.return_date:
            # Find other trips at the same hotel that overlap with the current date
            overlapping_trips = Trip.objects.filter(
                hotel=self.hotel,
                departure_date__lte=current_date,   # ORM query add start date
                return_date__gte=current_date       # ORM query add end date
            ).exclude(pk=self.pk)                   # don't count this trip again

            # Sum up the tickets from all overlapping trips on current_date
            other_tickets = sum(t.tickets for t in overlapping_trips)
            # Add tickets from this trip
            total_tickets = other_tickets + self.tickets

            # Check if total tickets (other trips + this trip) exceed hotel capacity
            if total_tickets > self.hotel.capacity:
                # Raise error and show available tickets
                raise ValidationError(
                    f'requested tickets: {total_tickets}, available: {self.hotel.capacity - other_tickets}')
            
            # Repeats check on next day of the trip
            current_date += timedelta(days=1)

    def clean(self):
        self.clean_dates()
        self.clean_tickets()
        self.clean_locations()
        self.clean_capacity_overlap()
        
    def save(self, *args, **kwargs):
        self.clean()

        super().save(*args, **kwargs)