from django.contrib import admin
from ..models import Booking

class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'trip', 'tickets_adult', 'tickets_child', 'booking_price', 'paid')
    actions = ['delete_unpaid_bookings_action']

    def delete_unpaid_bookings_action(self, request, queryset):
        try:
            for booking in queryset:
                if not booking.paid:
                    booking.delete()
            self.message_user(request, 'Unpaid bookings deleted ')
        except Exception as e:
            self.message_user(request, f'Error: {e}', level='error')

    def delete_model(self, request, obj):
        obj.delete()

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()

admin.site.register(Booking, BookingAdmin)
