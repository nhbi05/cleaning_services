from django import forms
from .models import Booking, ContactSubmission, Booking, ServiceOption, Service
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
class ContactForm(forms.ModelForm):
    """Form for contact submissions"""
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }

class BookingForm(forms.ModelForm):
    service = forms.ModelChoiceField(
        queryset=Service.objects.filter(is_active=True), 
        label='Service Type',
        required=True,
        empty_label='Select a Service',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_service'
        })
    )

    class Meta:
        model = Booking
        fields = [
            'service', 
            'service_option', 
            'customer_name', 
            'customer_email', 
            'customer_phone', 
            'booking_date', 
            'booking_time', 
            'address', 
            'city', 
            'state', 
            'zip_code', 
            'special_instructions'
        ]
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'booking_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'special_instructions': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'service_option': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_service_option'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Initially set service_option queryset to empty
        self.fields['service_option'].queryset = ServiceOption.objects.none()

        # Add a custom clean method to validate service options
        if 'service' in self.data:
            try:
                service_id = int(self.data.get('service'))
                self.fields['service_option'].queryset = ServiceOption.objects.filter(service_id=service_id)
            except (ValueError, TypeError):
                pass

    def clean(self):
        cleaned_data = super().clean()
        service = cleaned_data.get('service')
        service_option = cleaned_data.get('service_option')

        # Validate that service option matches the selected service
        if service and service_option:
            if service_option.service != service:
                raise ValidationError("Selected service option does not match the service type.")
        
        return cleaned_data
    
"""    def clean_booking_date(self):
    booking_date = self.cleaned_data.get('booking_date')
    if booking_date < timezone.now().date():
        raise ValidationError("Booking date cannot be in the past.")
    return booking_date

    def clean_customer_phone(self):
        phone = self.cleaned_data.get('customer_phone')
     # Add phone number validation logic
        return phone"""