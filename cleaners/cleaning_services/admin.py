from django.contrib import admin
from .models import (
    Service, ServiceOption, Booking, Testimonial,
    ContactSubmission, Feature
)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_from', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')

@admin.register(ServiceOption)
class ServiceOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'price', 'duration_hours', 'is_active')
    list_filter = ('service', 'is_active')
    search_fields = ('name', 'service__name')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'get_service_name', 'booking_date', 'booking_time', 'status')
    list_filter = ('status', 'booking_date', 'service_option__service')
    search_fields = ('customer_name', 'customer_email', 'address')
    readonly_fields = ('created_at', 'updated_at')
   
    def get_service_name(self, obj):
        return f"{obj.service_option.service.name} - {obj.service_option.name}"
    get_service_name.short_description = 'Service'

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'content')

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at',)

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'display_order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')