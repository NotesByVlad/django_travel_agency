from django.urls import path
from travel.views import (BookingCreateView, BookingUpdateView,
                        BookingDeleteView, PayBookingView,
                        booking_success)

urlpatterns = [
    path('booking/create/<int:pk>/', BookingCreateView.as_view(), name='booking_create'),
    path('booking/update/<int:pk>/', BookingUpdateView.as_view(), name='booking_update'),
    path('booking/delete/<int:pk>/', BookingDeleteView.as_view(), name='booking_delete'),
    path('booking/<int:pk>/pay/', PayBookingView.as_view(), name='booking_pay'),
    path('booking_success/', booking_success, name='booking_success'),
]
