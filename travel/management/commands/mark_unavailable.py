from django.core.management.base import BaseCommand
from datetime import date, timedelta
from travel.models import Trip

class Command(BaseCommand):
    help = "Marks trips as unavailable if they are starting tomorrow"

    def handle(self, *args, **kwargs):
        tomorrow = date.today() + timedelta(days=1)
        trips = Trip.objects.filter(departure_date=tomorrow, available=True)
        for trip in trips:
            trip.available = False
            trip.save()
        self.stdout.write(f"{trips.count()} trips marked as unavailable.")