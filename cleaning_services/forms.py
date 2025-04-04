from django import forms
from .models import Booking, ContactSubmission, Booking, Service,IndexContactSubmission
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError
class ContactForm(forms.ModelForm):
    """Form for contact submissions"""
    class Meta:
        model = ContactSubmission
        fields = ['first_name', 'last_name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }
class IndexContactForm(forms.ModelForm):
    class Meta:
        model = IndexContactSubmission
        fields = ['name', 'email', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'service_type',
            'service_details',
            'customer_name',
            'customer_email',
            'customer_phone',
            'booking_date',
            'booking_time',
            'address',
            'city',
            'special_instructions'
        ]
        widgets = {
            'service_type': forms.Select(choices=[
                ('', 'Select a Service'),
                ('Residential Cleaning', 'Residential Cleaning'),
                ('Commercial Cleaning', 'Commercial Cleaning'),
                ('Deep Cleaning', 'Deep Cleaning'),
                ('Move-In/Move-Out', 'Move-In/Move-Out'),
            ], attrs={'class': 'form-control'}),
            'booking_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'booking_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'special_instructions': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add form-control class to all fields
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'

    def clean_booking_date(self):
        booking_date = self.cleaned_data.get('booking_date')
        if booking_date < timezone.now().date():
            raise ValidationError("Booking date cannot be in the past.")
        return booking_date