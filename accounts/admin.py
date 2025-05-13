from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()

# Create a custom Admin class for your CustomUser model
class CustomUserAdmin(UserAdmin):
    # Add the fields you want to display in the list view (when you see all users)
    list_display = (
        'username',
        'email',
        'name',
        'surname',
        'country',
        'is_active',
        'is_staff',
    )

    # Add the fields you want to be able to filter by in the list view
    list_filter = (
        'is_active',
        'is_staff',
        'groups', # Keep this if you use groups for permissions
    )

    # Add the fields you want to be able to search by in the list view
    search_fields = (
        'username',
        'email',
    )

    # Define the fields that appear in the form when adding or editing a user
    # You can simplify this fieldsets to include only the essential fields
    # while still inheriting from UserAdmin for standard user management.
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('email',)}), # Only include email here
        (('Permissions'), {'fields': (
            'is_active',
            'is_staff',
            'is_superuser', # Keep superuser for admin control
            'groups',
            'user_permissions',
        )}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}), # Keep these for reference
    )

    # You can also define the ordering of users in the list view
    ordering = ('username',)

# Register your CustomUser model with your custom Admin class
admin.site.register(User, CustomUserAdmin)