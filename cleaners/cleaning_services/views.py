# cleaning/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import (
    Service, ServiceOption, Booking, Testimonial, 
    ContactSubmission, Feature,
)
from .forms import (
    ContactForm, BookingForm
)

def home(request):
    """View for the home page"""
    services = Service.objects.filter(is_active=True)
    testimonials = Testimonial.objects.filter(is_active=True)
    features = Feature.objects.filter(is_active=True)
    
    
    
    context = {
        'services': services,
        'testimonials': testimonials,
        'features': features,
       
    }
    return render(request, 'cleaning_services/index.html', context)

def about(request):
    """View for the about page"""
    features = Feature.objects.filter(is_active=True)
    return render(request, 'cleaning_services/about.html', {'features': features})

def services_view(request):
    """View for the services page"""
    services = Service.objects.filter(is_active=True)
    return render(request, 'cleaning_services/services.html', {'services': services})

def contact(request):
    """View for the contact page"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_submission = form.save()
            
            # Send email notification
            send_mail(
                subject=f'New Contact Form Submission from {contact_submission.name}',
                message=f"Name: {contact_submission.name}\nEmail: {contact_submission.email}\nPhone: {contact_submission.phone}\nMessage: {contact_submission.message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['admin@cleanfuture.com'],  # Change to your admin email
                fail_silently=False,
            )
            
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'cleaning_services/contact.html', {'form': form})

def booking_view(request):
    """View for creating a new booking"""
    if request.method == 'POST':
        # Create form with POST data
        form = BookingForm(request.POST)
        
        if form.is_valid():
            # Save the booking
            booking = form.save()
            
            # Send confirmation email
            try:
                send_mail(
                    subject='Your Booking Confirmation',
                    message=f"Thank you for booking {booking.service_option.service.name} - {booking.service_option.name} on {booking.booking_date.strftime('%A, %B %d, %Y')} at {booking.booking_time.strftime('%I:%M %p')}.\n\n"
                            f"We will contact you soon to confirm your appointment.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[booking.customer_email],
                    fail_silently=False,
                )
            except Exception as e:
                # Log the email error, but still show success to the user
                print(f"Email sending failed: {e}")
            
            # Redirect to a success page or booking list
            return redirect('my_bookings')
    form = BookingForm(initial={
            'service': Service.objects.filter(is_active=True).first()
        })
    
    context = {
        'form': form,
        'services': Service.objects.filter(is_active=True)
    }
    
    return render(request, 'cleaning_services/booking.html', context)

def my_bookings(request):
    """View for displaying user's bookings"""
    bookings = Booking.objects.filter(customer_email=request.POST.get('email')).order_by('-booking_date', '-booking_time')
    return render(request, 'cleaning_services/bookings.html', {'bookings': bookings})

def cancel_booking(request, booking_id):
    """View for cancelling a booking"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    if booking.status == 'pending' or booking.status == 'confirmed':
        booking.status = 'cancelled'
        booking.save()
    
    return redirect('my_bookings')


@require_POST
def get_service_options(request):
    """AJAX view to get service options based on selected service"""
    service_id = request.POST.get('service_id')
    options = ServiceOption.objects.filter(service_id=service_id, is_active=True)
    
    options_data = []
    for option in options:
        options_data.append({
            'id': option.id,
            'name': option.name,
            'description': option.description,
            'price': float(option.price),
            'duration': float(option.duration_hours)
        })
    
    return JsonResponse({'options': options_data})