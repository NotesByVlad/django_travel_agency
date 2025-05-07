import re
from django import forms
from django.core.exceptions import ValidationError

TAG_RE = re.compile(r'<[^>]+>')  # Matches anything between < >

def sanitize_input(value: str) -> str:
    value = value.strip()                      # Remove leading/trailing whitespace
    value = TAG_RE.sub('', value)              # Strip HTML tags
    value = re.sub(r'(javascript:|on\w+=)', '', value, flags=re.IGNORECASE)  # Strip JS-related patterns
    return value

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'autofocus': 'autofocus',
            'autocomplete': 'name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'autocomplete': 'off'
        })
    )

    def clean_name(self):
        name = sanitize_input(self.cleaned_data['name'])
        if not name:
            raise ValidationError("Name cannot be empty after cleaning.")
        return name

    def clean_email(self):
        email = sanitize_input(self.cleaned_data['email']).lower()
        return email

    def clean_message(self):
        message = sanitize_input(self.cleaned_data['message'])
        if not message:
            raise ValidationError("Message cannot be empty after cleaning.")
        return message