from django.contrib import admin
from django.utils.html import format_html
from ..models import Continent, Country, City, Hotel, HotelImages, Airport

# --- CONTINENT ---
class ContinentAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_preview')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Image'

admin.site.register(Continent, ContinentAdmin)

# --- COUNTRY ---
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'continent', 'image_preview')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Image'

    class Meta:
        verbose_name_plural = 'Countries'

admin.site.register(Country, CountryAdmin)

# --- CITY ---
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'image_preview')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Image'

admin.site.register(City, CityAdmin)

# --- HOTEL ---
class HotelImagesInline(admin.TabularInline):
    model = HotelImages
    extra = 1

class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'stars', 'capacity',)
    inlines = [HotelImagesInline]

admin.site.register(Hotel, HotelAdmin)

# --- AIRPORT ---
class AirportAdmin(admin.ModelAdmin):
    list_display = ('name', 'city',)

admin.site.register(Airport, AirportAdmin)
