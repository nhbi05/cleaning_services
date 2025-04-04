# cleaning/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST

from .models import (
    Service,  Booking,  
    ContactSubmission,IndexContactSubmission
)
from .forms import (
    ContactForm, BookingForm,IndexContactForm
)

def home(request):
    return render(request, 'cleaning_services/index.html')


    
def about(request):
    """View for the about page"""

    return render(request, 'cleaning_services/about.html', {})

def services_view(request):
    """View for the services page"""
    services = Service.objects.filter(is_active=True)
    return render(request, 'cleaning_services/services.html', {'services': services})

from django.contrib import messages  # Import the messages framework

def contact(request):
    """View for the contact page"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                contact_submission = form.save()
                # Send email notification
                send_mail(
                    subject=f'New Contact Form Submission: {contact_submission.subject}',
                    message=f"Name: {contact_submission.first_name} {contact_submission.last_name}\nEmail: {contact_submission.email}\nPhone: {contact_submission.phone}\nSubject: {contact_submission.subject}\nMessage: {contact_submission.message}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['adcleanfuture1@gmail.com'],  # Change to your admin email
                    fail_silently=False,
                )
                
                # Add success message
                messages.success(request, "Thank you! Your message has been sent successfully. We'll get back to you soon.")
                
            except Exception as e:
                # Add error message
                messages.error(request, "There was a problem sending your message. Please try again later.")
                print(f"Error in contact form: {e}")
        else:
            # Form validation errors
            messages.error(request, "Please correct the errors in the form and try again.")
    else:
        form = ContactForm()
    
    return render(request, 'cleaning_services/contact.html', {'form': form})

from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import BookingForm

def booking_view(request):
    """View for the booking page"""
    form = BookingForm(request.POST or None)  # Initialize form with POST data if available

    if request.method == 'POST':
        if form.is_valid():
            try:
                booking = form.save()
                
                # Send email notification
                send_mail(
                    subject=f'New Booking Request from {booking.customer_name}',
                    message=f"Service: {booking.service_type}\n"
                            f"Details: {booking.service_details}\n"
                            f"Name: {booking.customer_name}\n"
                            f"Email: {booking.customer_email}\n"
                            f"Phone: {booking.customer_phone}\n"
                            f"Date: {booking.booking_date}\n"
                            f"Time: {booking.booking_time}\n"
                            f"Address: {booking.address}, {booking.city}\n"
                            f"Special Instructions: {booking.special_instructions}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['adcleanfuture1@gmail.com'],  # Change to your admin email
                    fail_silently=False,
                )

                # Add success message
                messages.success(request, "Thank you! Your booking request has been submitted successfully. We'll contact you shortly to confirm your appointment.")

                # Instead of redirecting, reload the same page with a new blank form
                form = BookingForm()  # Reset the form

            except Exception as e:
                # Add error message
                messages.error(request, "There was a problem processing your booking. Please try again later.")
                print(f"Error in booking form: {e}")
        else:
            # Form validation errors
            messages.error(request, "Please correct the errors in the form and try again.")

    return render(request, 'cleaning_services/booking.html', {'form': form})





