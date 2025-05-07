from django import forms
from travel.models import Booking


# ModelForm -> create or update an instance of a model
YES_NO_CHOICES = [('True', 'Yes'), ('False', 'No')]
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
            'tickets_adult': forms.NumberInput(
                attrs={ 'id': 'id_booking_tickets_adult',
                        'min': '1',
                        'max': '50',
                        'maxlength': '2',
            }),
            'tickets_child': forms.NumberInput(
                attrs={ 'id': 'id_booking_tickets_child',
                        'min': '0',
                        'max': '50',
                        'maxlength': '2',
            }),
            'trip': forms.HiddenInput(),
            'meal_plan': forms.Select(
                attrs={ 'id': 'id_booking_meal_plan',
            }),
            'wants_flight': forms.Select(
                choices=YES_NO_CHOICES, 
                attrs={ 'id': 'id_booking_wants_flight'
            }),
            
            'from_airport': forms.Select(
                attrs={ 'id': 'id_booking_from_airport',
            }),

            'wants_airport_pickup': forms.Select(
                choices=YES_NO_CHOICES, 
                attrs={ 'id': 'id_booking_airport_pickup'
            }),
            
            'wants_airport_dropoff': forms.Select(
                choices=YES_NO_CHOICES, 
                attrs={ 'id': 'id_booking_airport_dropoff'
            }),
            
            'wants_car_rental': forms.Select(
                choices=YES_NO_CHOICES, 
                attrs={ 'id': 'id_booking_car_rental'
            }),
            
            'car_rental_days': forms.NumberInput(
                attrs={ 'id': 'id_booking_car_rental_days',
                        'min': '0',
                        'max': '30',
                        'maxlength': '2',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['wants_flight'].initial = 'True'
        self.fields['wants_airport_pickup'].initial = 'False'
        self.fields['wants_airport_dropoff'].initial = 'False'
        self.fields['wants_car_rental'].initial = 'False'

    def clean_tickets(self):
        """Validate the total number of tickets (adult + child)."""
        tickets_adult = self.cleaned_data.get('tickets_adult') or 0
        tickets_child = self.cleaned_data.get('tickets_child') or 0
        trip = self.cleaned_data.get('trip')

        if trip:
            total_requested = tickets_adult + tickets_child
            if total_requested > trip.tickets:
                error_msg = f"Only {trip.tickets} tickets left on this trip."
                self.add_error('tickets_adult', error_msg)
                self.add_error('tickets_child', error_msg)

    def clean_airport(self):
        """Validate departure airport when flight is selected."""
        wants_flight = self.cleaned_data.get('wants_flight')
        from_airport = self.cleaned_data.get('from_airport')

        if wants_flight and not from_airport:
            self.add_error('from_airport', "Please select a departure airport.")
        
        return from_airport
    
    def clean_car_rental(self):
        """Validate car rental days."""
        wants_car_rental = self.cleaned_data.get('wants_car_rental')
        car_rental_days = self.cleaned_data.get('car_rental_days')
        trip = self.cleaned_data.get('trip')

        if wants_car_rental and car_rental_days == 0:
            self.add_error('car_rental_days', 'Please select a number of days for renting a car.')
        
        if wants_car_rental and trip and car_rental_days > trip.calculate_duration():
            self.add_error('car_rental_days', 'Please select a valid number of days for renting.')

        return car_rental_days

    def clean(self):
        """Run general form validations."""
        cleaned_data = super().clean()

        self.clean_tickets()
        self.clean_airport()
        self.clean_car_rental()

        return cleaned_data