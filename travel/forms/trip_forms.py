from django import forms
from travel.models import Continent, Country, City, Airport
from datetime import date, timedelta

class TripSearchForm(forms.Form):
    continent = forms.ModelChoiceField(
        queryset=Continent.objects.all(),
        required=False,
        empty_label="Continent",
        widget=forms.Select(attrs={'autocomplete': 'off'}),
    )
    
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        required=False,
        empty_label="Country",
        widget=forms.Select(attrs={'autocomplete': 'off'}),
    )
    
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        required=False,
        empty_label="City",
        widget=forms.Select(attrs={'autocomplete': 'off'}),
    )

    departure_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date',
                                      'min': (date.today() + timedelta(days=1)).isoformat(),
                                      'autocomplete': 'off'}),
        label="Departure Date",
    )

    return_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date',
                                      'min': (date.today() + timedelta(days=1)).isoformat(),
                                      'autocomplete': 'off'}),
        label="Return Date",
    )
    wants_flight = forms.ChoiceField(
        choices=[('yes', 'Yes'), ('no', 'No')],
        required=False,
        label="Do you want flight tickets?",
        initial='yes',
        widget=forms.Select(attrs={'autocomplete': 'off'})
    )
    from_airport = forms.ModelChoiceField(
        queryset=Airport.objects.all(),
        required=False,
        empty_label="Select your departure airport",
        label="From Airport",
        widget=forms.Select(attrs={'autocomplete': 'off'}),
    )
    tickets_adults = forms.IntegerField(
        required=False,
        min_value=1,
        label="Tickets for Adults",
        widget=forms.NumberInput(attrs={'min': '1',
                                        'autocomplete': 'off'})

    )
    
    tickets_children = forms.IntegerField(
        required=False,
        min_value=0,
        label="Tickets for Children",
        widget=forms.NumberInput(attrs={'min': '0',
                                        'autocomplete': 'off'})
    )
    budget = forms.DecimalField(
        required=False,
        label="Budget",

        widget=forms.NumberInput(attrs={'min': '0',
                                        'autocomplete': 'off'})
    )

    def clean_tickets(self):
        """Validate that at least one adult is selected when children are selected"""
        cleaned_data = super().clean()
        adults = cleaned_data.get('tickets_adults')
        children = cleaned_data.get('tickets_children')

        if (adults is None or adults < 1) and (children and children > 0):
            raise forms.ValidationError("At least one adult is required if children are selected.")
        
        return cleaned_data

    def clean_flight_and_airport(self):
        """Validate that if flight is required, airport must be selected if budget is set."""
        cleaned_data = super().clean()
        wants_flight = cleaned_data.get('wants_flight')
        from_airport = cleaned_data.get('from_airport')
        budget = cleaned_data.get('budget')

        if wants_flight == 'yes' and not from_airport and budget is not None:
            raise forms.ValidationError("Please select a departure airport to calculate accurate flight costs for your budget.")
        
        return cleaned_data

    def clean_departure_date(self):
        """Ensure the departure date is from tomorrow onwards."""
        dep_date = self.cleaned_data.get('departure_date')
        if dep_date and dep_date < date.today() + timedelta(days=1):
            raise forms.ValidationError("Departure date must be from tomorrow onwards.")
        return dep_date

    def clean(self):
        """Run general form validations."""
        cleaned_data = super().clean()
        self.clean_tickets()
        self.clean_flight_and_airport()

        return cleaned_data