from django.contrib import admin
from django.utils.html import format_html
from travel.models import Invoice

from django.urls import reverse

# --- INVOICE ---
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'invoice_number',
        'booking_user',
        'payment_date',
        'booking',
        'booking_trip',
        'booking_price',
        'booking_paid',
    )
    readonly_fields = (
        'payment_date',
        'booking_user',
        'booking_email',
        'booking',
        'booking_trip',
        'booking_tickets_adult',
        'booking_tickets_child',
        'booking_meal_plan',
        'booking_price',
        'booking_paid',
    )

    def booking_user(self, obj):
        return obj.booking.user 
    booking_user.short_description = 'User'

    def booking_email(self, obj):
        return obj.booking.user.email
    booking_email.short_description = 'Email'

    def booking_trip(self, obj):
        trip = obj.booking.trip
        url = reverse("admin:travel_trip_change", args=[trip.pk])
        return format_html('<a href="{}">{}</a>', url, trip)
    booking_trip.short_description = 'Trip'

    def booking_tickets_adult(self, obj):
        return obj.booking.tickets_adult
    booking_tickets_adult.short_description = 'Adult Tickets'

    def booking_tickets_child(self, obj):
        return obj.booking.tickets_child
    booking_tickets_child.short_description = 'Child Tickets'

    def booking_meal_plan(self, obj):
        return obj.booking.get_meal_plan_display()
    booking_meal_plan.short_description = 'Meal Plan'

    def booking_price(self, obj):
        return f' $ {obj.booking.booking_price:,.0f}'
    booking_price.short_description = 'Booking Price'

    def booking_paid(self, obj):
        return obj.booking.paid
    booking_paid.short_description = 'Paid?'

admin.site.register(Invoice, InvoiceAdmin)