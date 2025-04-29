from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

### Continent ###
class Continent(models.Model):
    name = models.CharField(max_length=30, unique=True, help_text='Continent name')
    description = models.TextField(null=True, blank=True, help_text='Continent description')
    image = models.ImageField(upload_to='continent_images/', blank=True, null=True)

    def __str__(self):
        return self.name
    

### Country ###
class Country(models.Model):
    class Meta:
        verbose_name_plural = 'Countries'
        
    name = models.CharField(max_length=30, unique=True, help_text='Country name')
    description = models.TextField(null=True, blank=True, help_text='Country description')
    image = models.ImageField(upload_to='country_images/', blank=True, null=True)
    continent = models.ForeignKey(Continent, related_name='countries', 
                                  on_delete=models.CASCADE, help_text='Continent')

    def __str__(self):
        return self.name


### City ###
class City(models.Model):
    class Meta:
        verbose_name_plural = "Cities"

    name = models.CharField(max_length=30, help_text='City name')
    description = models.TextField(null=True, blank=True, help_text='City description')
    image = models.ImageField(upload_to='city_images/', blank=True, null=True)
    country = models.ForeignKey(Country, related_name='cities', 
                                on_delete=models.CASCADE, help_text='Country')

    car_rental_option = models.BooleanField(help_text='Car rental option')
    car_rental_cost = models.IntegerField(null=True, blank=True, 
                                          help_text='Car rental cost per day in this City')

    def __str__(self):
        return self.name


### Hotel ###
class Hotel(models.Model):
    name = models.CharField(max_length=100, help_text='Hotel name')
    stars = models.PositiveIntegerField(validators=
                                        [MinValueValidator(1),
                                         MaxValueValidator(5)], help_text='Hotel Stars')

    description = models.TextField(help_text='Description of the hotel')
    city = models.ForeignKey(City, related_name='hotels', 
                             on_delete=models.CASCADE, help_text='City')
    capacity = models.PositiveIntegerField(help_text='Hotel capacity reserved for our agency')
    
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2,
                                        help_text= 'Base price per day')
    
    # Meal plans prices
    bb_price = models.DecimalField(max_digits=10, decimal_places=2,
        null=True, blank=True,
        help_text='Additional price per day for Bed & Breakfast')
    
    hb_price = models.DecimalField(max_digits=10, decimal_places=2,
        null=True, blank=True,
        help_text='Additional price per day for Half Board')
    
    fb_price = models.DecimalField(max_digits=10, decimal_places=2,
        null=True, blank=True,
        help_text='Additional price per day for Full Board')
    
    ai_price = models.DecimalField(max_digits=10, decimal_places=2,
        null=True, blank=True,
        help_text='Additional price per day for All Inclusive')

    def __str__(self):
        return self.name
    
class HotelImages(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hotel_images/')

    def __str__(self):
        return f"Image for {self.hotel.name}"


### Airport ###
class Airport(models.Model):
    name = models.CharField(max_length=100, help_text='Airport name')
    code = models.CharField(max_length=3, help_text='IATA code, 3 letter unique code for airports')
    standard_plane_ticket = models.IntegerField(default=100, help_text='Ticket price')

    city = models.ForeignKey(City, related_name='airports', on_delete=models.CASCADE,
                             help_text='City')

    # Airport Services
    airport_pick_up_cost = models.PositiveIntegerField(default=10,
        help_text='Price picking up from airport')
    
    airport_drop_off_cost = models.PositiveIntegerField(default=10,
        help_text='Price for dropping of to the airport')

    # Flight cost for different country / continent
    # def calculate_plane_ticket_cost(self, from_country, from_continent, 
    #                             to_country, to_continent):
        
    #     price_outside_country = 0.30   # 30 % more
    #     price_outside_continent = 0.50 # 50 % more

    #     is_same_continent = from_continent == to_continent
    #     is_same_country = from_country == to_country

    #     if is_same_continent and not is_same_country:
    #         return self.standard_plane_ticket + (price_outside_country * self.standard_plane_ticket)
    #     elif not is_same_continent:
    #         return self.standard_plane_ticket + (price_outside_continent * self.standard_plane_ticket)
        
    #     return self.standard_plane_ticket

    def __str__(self):
        return self.name