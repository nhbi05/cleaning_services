from django.urls import path
from . import views
#from django.contrib.auth import views as auth_views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services_view, name='services'),
    path('contact/', views.contact, name='contact'),
    
    # Booking-related paths
    path('booking/', views.booking_view, name='booking'),
    #path('my-bookings/', views.my_bookings, name='my_bookings'),
    #path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    
    # Service options path with service_id parameter
     #path('get-service-options/', views.get_service_options, name='get_service_options'),
]