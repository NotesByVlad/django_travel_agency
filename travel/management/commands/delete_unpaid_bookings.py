from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from travel.models import Booking

class Command(BaseCommand):
    help = 'Deletes unpaid bookings older than 1 hour'

    def handle(self, *args, **kwargs):
        one_hour_ago = timezone.now() - timedelta(hours=1)
        old_unpaid_bookings = Booking.objects.filter(paid=False, booking_date__lt=one_hour_ago)
        count = old_unpaid_bookings.count()
        old_unpaid_bookings.delete()

        self.stdout.write(self.style.SUCCESS(f'{count} unpaid booking(s) deleted.'))