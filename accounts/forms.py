from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username__iexact=username).exists():
            raise ValidationError('This username is already taken')
        return username
    


from django.forms import ModelForm
from .models import CustomUser
from django import forms
from travel.models import Country, City
class CustomUserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'surname', 'country', 'city']

    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'autofocus': 'autofocus',
            'autocomplete': 'name'
        })
    )

    surname = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'autocomplete': 'surname'
        })
    )

    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        empty_label="Select a country",
        required=False
    )

    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        empty_label="Select a city",
        required=False
    )

    # When initializing the form, populate the fields with data from user
    def __init__(self, *args, **kwargs):
        user = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        # Set default city queryset to empty
        self.fields['city'].queryset = City.objects.none()

        # Handle POST request (country selection)
        self.fields['city'].queryset = City.objects.none()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(country_id=country_id)
            except (ValueError, TypeError):
                pass
        elif user and user.country:
            self.fields['city'].queryset = City.objects.filter(country=user.country)

        # Populate other fields
        if user:
            self.fields['name'].initial = user.name
            self.fields['surname'].initial = user.surname
            self.fields['country'].initial = user.country
            self.fields['city'].initial = user.city