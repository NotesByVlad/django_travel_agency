from django.contrib import admin
from travel.models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'user', 'replied')
    list_filter = ('created_at', 'replied')
    search_fields = ('name', 'email', 'message')

    readonly_fields = ('user', 'name', 'email', 'message', 'created_at', 'replied_at', 'replied')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        """Allow changing only to reply, not to modify original data."""
        if request.method in ['POST', 'PUT'] and obj:
            readonly = {'name', 'email', 'message'}
            for field in readonly:
                if field in request.POST and request.POST[field] != getattr(obj, field):
                    return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return True