from django.contrib import admin
from ..models import Booking
from django.contrib import admin
from django.contrib import messages

class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'trip', 'tickets_adult', 'tickets_child', 'booking_price', 'paid')
    actions = ['delete_unpaid_bookings_action']

    def delete_unpaid_bookings_action(self, request, queryset):
        unpaid_bookings = queryset.filter(paid=False)
        count = unpaid_bookings.count()
        if count > 0:
            unpaid_bookings.delete()
            self.message_user(request, f'{count} unpaid booking(s) deleted.', level=messages.SUCCESS)
        else:
            self.message_user(request, 'No unpaid bookings selected for deletion.', level=messages.WARNING)

    def delete_model(self, request, obj):
        obj.delete()

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()

    def has_delete_permission(self, request, obj=None):
        """
        Override delete permission to prevent deletion of paid bookings.
        """
        if obj and obj.paid:
            return False  # Prevent deletion of paid bookings
        return super().has_delete_permission(request, obj)

admin.site.register(Booking, BookingAdmin)