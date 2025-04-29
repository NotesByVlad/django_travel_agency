from django.contrib import admin
from ..models import Trip

class TripAdmin(admin.ModelAdmin):
    list_display = ('tickets', 'departure_date', 'return_date', 'hotel', 'city', 'airport',)
    readonly_fields = ('city', 'airport')

admin.site.register(Trip, TripAdmin)
