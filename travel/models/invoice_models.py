from django.db import models
from .booking_models import Booking
from django.utils import timezone


# # # Invoice Model # # #

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    payment_date = models.DateTimeField(default=timezone.now)

    # Booking related to invoice
    booking = models.OneToOneField(Booking,on_delete=models.SET_NULL, null=True, related_name='invoice')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.booking:
            self.booking.paid = True
            self.booking.save()

    def generate_invoice_number(self):
        # Get the first 3 characters of the city name
        city_code = self.booking.trip.city.name[:3].upper()

        # Get the latest invoice number for the same city and trip
        latest_invoice = Invoice.objects.filter(booking__trip=self.booking.trip).order_by('-invoice_number').first()

        # Get the last number in the sequence, or start at 1 if there are no invoices yet
        if latest_invoice:
            last_number = int(latest_invoice.invoice_number[-1])  # Assuming last character is the number
            next_number = last_number + 1
        else:
            next_number = 1

        # Create the new invoice number
        invoice_number = f"INV{city_code}{next_number}"

        return invoice_number

    def __str__(self):
        return f'Invoice {self.invoice_number}'