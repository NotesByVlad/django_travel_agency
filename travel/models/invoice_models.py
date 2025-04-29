from django.db import models
from .booking_models import Booking
from django.utils import timezone


# # # Invoice Model # # #

class Invoice(models.Model):
    payment_date = models.DateTimeField(default=timezone.now)

    # Booking related to invoice
    booking = models.OneToOneField(Booking,on_delete=models.SET_NULL, null=True, related_name='invoice')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.booking:
            self.booking.paid = True
            self.booking.save()

    def __str__(self):
        return f'Invoice for {self.booking.trip}. {self.payment_date}'