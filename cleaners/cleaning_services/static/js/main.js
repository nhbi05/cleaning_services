
// Navbar Scroll Effect
window.addEventListener('scroll', function() {
    const navbar = document.getElementById('navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Mobile Menu Toggle
document.getElementById('menuToggle').addEventListener('click', function() {
    document.getElementById('navLinks').classList.toggle('active');
});

// Scroll Reveal Animation
window.addEventListener('scroll', function() {
    const reveals = document.querySelectorAll('.reveal');
    
    for (let i = 0; i < reveals.length; i++) {
        const windowHeight = window.innerHeight;
        const revealTop = reveals[i].getBoundingClientRect().top;
        const revealPoint = 150;
        
        if (revealTop < windowHeight - revealPoint) {
            reveals[i].classList.add('active');
        }
    }
});

// Testimonial Slider
const dots = document.querySelectorAll('.testimonial-dot');
const slider = document.getElementById('testimonialSlider');

dots.forEach(dot => {
    dot.addEventListener('click', function() {
        const index = this.getAttribute('data-index');
        
        // Update active dot
        dots.forEach(d => d.classList.remove('active'));
        this.classList.add('active');
        
        // Slide to the selected testimonial
        const slideWidth = slider.clientWidth;
        slider.scrollTo({
            left: slideWidth * index,
            behavior: 'smooth'
        });
    });
});

// Newsletter Form AJAX Submission
document.getElementById('newsletterForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const form = this;
    const formData = new FormData(form);
    
    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': formData.get('csrfmiddlewaretoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        if (data.status === 'success' || data.status === 'info') {
            form.reset();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    });
});
document.addEventListener('DOMContentLoaded', function() {
    const serviceSelect = document.getElementById('id_service');
    const serviceOptionSelect = document.getElementById('id_service_option');

    serviceSelect.addEventListener('change', function() {
        const serviceId = this.value;
        
        fetch(`/get-service-options/${serviceId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            serviceOptionSelect.innerHTML = '<option value="">Select a Service Option</option>';
            data.options.forEach(option => {
                const optionElement = document.createElement('option');
                optionElement.value = option.id;
                optionElement.textContent = `${option.name} - $${option.price} (${option.duration} hrs)`;
                serviceOptionSelect.appendChild(optionElement);
            });
        });
    });
});
