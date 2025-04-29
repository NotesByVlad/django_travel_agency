from django import forms
from travel.models import Booking


# ModelForm -> create or update an instance of a model

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['trip', 'meal_plan', 
                'tickets_adult', 'tickets_child', 
                'wants_flight', 'from_airport',
                'wants_airport_pickup',
                'wants_airport_dropoff',
                'wants_car_rental', 'car_rental_days'
                ]

        widgets = {
            'trip': forms.HiddenInput(),
            'meal_plan': forms.Select(attrs={
                'id': 'id_booking_meal_plan',
            }),
            'tickets_adult': forms.NumberInput(attrs={
                'id': 'id_booking_tickets_adult',
            }),
            'tickets_child': forms.NumberInput(attrs={
                'id': 'id_booking_tickets_child',
            }),
            'wants_flight': forms.CheckboxInput(attrs={
                'id': 'id_booking_wants_flight',
            }),
            'from_airport': forms.Select(attrs={
                'id': 'id_booking_from_airport',
            }),
            'wants_airport_pickup': forms.CheckboxInput(attrs={
                'id': 'id_booking_airport_pickup',
            }),
            'wants_airport_dropoff': forms.CheckboxInput(attrs={
                'id': 'id_booking_airport_dropoff',
            }),
            'wants_car_rental': forms.CheckboxInput(attrs={
                'id': 'id_booking_car_rental',
            }),
            'car_rental_days': forms.NumberInput(attrs={
                'id': 'id_booking_car_rental_days',
            }),
        }
        # front-end -> By default: Django auto-generates id="id_<field_name>"

    def clean_car_rental(self):
        """Validate car rental days."""
        wants_car_rental = self.cleaned_data.get('wants_car_rental')
        car_rental_days = self.cleaned_data.get('car_rental_days')
        trip = self.cleaned_data.get('trip')

        # Validate if car rental is selected and car rental days are provided
        if wants_car_rental and car_rental_days == 0:
            self.add_error('car_rental_days', 'Please select a number of days for renting a car.')
        
        # Validate that car rental days do not exceed trip duration
        if wants_car_rental and trip and car_rental_days > trip.calculate_duration():
            self.add_error('car_rental_days', 'Please select a valid number of days for renting.')

        return car_rental_days

    def clean_airport(self):
        """Validate departure airport when flight is selected."""
        wants_flight = self.cleaned_data.get('wants_flight')
        from_airport = self.cleaned_data.get('from_airport')

        # Ensure an airport is selected if the flight is chosen
        if wants_flight and not from_airport:
            self.add_error('from_airport', "Please select a departure airport.")
        
        return from_airport

    def clean(self):
        """Run general form validations."""
        cleaned_data = super().clean()

        # Perform individual clean methods
        self.clean_car_rental()
        self.clean_airport()

        return cleaned_data