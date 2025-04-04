from django.contrib import admin
from .models import (
    Service,  Booking,
    ContactSubmission, IndexContactSubmission
)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_from', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')


from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'service_type', 'booking_date', 'status')
    list_filter = ('status', 'booking_date', 'service_type')
    search_fields = ('customer_name', 'customer_email', 'address')
    readonly_fields = ('created_at', 'updated_at')
    """def get_service_name(self, obj):
        return f"{obj.service_option.service.name} - {obj.service_option.name}"
    get_service_name.short_description = 'Service'
"""

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'subject', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'message')
    list_filter = ('subject', 'created_at')

@admin.register(IndexContactSubmission)
class IndexContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email', 'message')
    list_filter = ('created_at',)
