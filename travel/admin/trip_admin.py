from django.contrib import admin, messages
from ..models import Trip
from django.utils import timezone

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('city', 'tickets', 'departure_date', 'return_date', 'hotel', 'airport', 'available')
    list_filter = ('available', 'promoted', 'departure_date', 'return_date', 'hotel', 'city', 'airport')
    search_fields = ('hotel__name', 'city__name')
    readonly_fields = ('city', 'airport', 'available')
    ordering = ('-departure_date',)
    date_hierarchy = 'departure_date'
    actions = ['mark_selected_unavailable']
    
    def get_readonly_fields(self, request, obj=None):
        if obj and not obj.available:
            # Make ALL fields readonly
            return [field.name for field in self.model._meta.fields]
        return super().get_readonly_fields(request, obj)

    def has_change_permission(self, request, obj=None):
        if obj and not obj.available:
            # Prevent form from being saved/edited
            return False
        return super().has_change_permission(request, obj)
    
    @admin.action(description='Mark selected trips as unavailable if they start tomorrow')
    def mark_selected_unavailable(self, request, queryset):
        tomorrow = timezone.now().date() + timezone.timedelta(days=1)
        trips_to_update = queryset.filter(departure_date=tomorrow, available=True)
        updated_count = trips_to_update.update(available=False)

        self.message_user(request, f"{updated_count} trip(s) were marked as unavailable.",
            level=messages.SUCCESS
        )