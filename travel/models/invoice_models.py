from django.db import models
from .booking_models import Booking
from django.utils import timezone


# # # Invoice Model # # #

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    payment_date = models.DateTimeField(default=timezone.now)

    # Booking related to invoice
    booking = models.OneToOneField(Booking,on_delete=models.SET_NULL, null=True, related_name='invoice')



    def generate_invoice_number(self):
        # Replace 'BKN' with 'INV' from booking number
        if not self.booking or not self.booking.booking_number:
            raise ValueError("Booking or booking_number is missing")

        booking_number = self.booking.booking_number
        invoice_count = Invoice.objects.count() + 1  # len of Invoice table

        core = booking_number[3:]  # remove 'BKN'
        return f"INV{invoice_count}{core}"
    
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = self.generate_invoice_number()

        super().save(*args, **kwargs)

        if self.booking and not self.booking.paid:
            self.booking.paid = True
            self.booking.save()


    def __str__(self):
        return f'Invoice {self.invoice_number}'