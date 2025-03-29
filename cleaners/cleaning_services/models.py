from django.db import models
from django.utils import timezone

class Service(models.Model):
    """Model for cleaning services offered by the company"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text='Emoji or icon class')
    price_from = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ServiceOption(models.Model):
    """Model for specific options within services (e.g., Small, Medium, Large home)"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='options')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_hours = models.DecimalField(max_digits=4, decimal_places=1, default=2.0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.service.name} - {self.name}"

class Booking(models.Model):
    """Model for customer bookings"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
   
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    service_option = models.ForeignKey(ServiceOption, on_delete=models.PROTECT)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    special_instructions = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    class Meta:
        ordering = ['-booking_date', '-booking_time']
   
    def __str__(self):
        return f"{self.customer_name} - {self.service_option.service.name} on {self.booking_date}"

class Testimonial(models.Model):
    """Customer testimonials"""
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return f"Testimonial by {self.name}"

class ContactSubmission(models.Model):
    """Contact form submissions"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
   
    class Meta:
        ordering = ['-created_at']
   
    def __str__(self):
        return f"Contact from {self.name} on {self.created_at.strftime('%Y-%m-%d')}"

class Feature(models.Model):
    """Features showcased in 'Why Choose Us' section"""
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text='Emoji or icon class')
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveSmallIntegerField(default=0)
   
    class Meta:
        ordering = ['display_order']
   
    def __str__(self):
        return self.title