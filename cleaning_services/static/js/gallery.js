// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Navbar scroll effect
    const navbar = document.getElementById('navbar');
    const menuToggle = document.getElementById('menuToggle');
    const navLinks = document.getElementById('navLinks');
    
    // Scroll effect for navbar
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
    
    // Mobile menu toggle
    menuToggle.addEventListener('click', function() {
        navLinks.classList.toggle('active');
    });
    
    // Scroll animation for elements
    function revealOnScroll() {
        const reveals = document.querySelectorAll('.reveal');
        
        reveals.forEach(element => {
            const windowHeight = window.innerHeight;
            const elementTop = element.getBoundingClientRect().top;
            const elementVisible = 150;
            
            if (elementTop < windowHeight - elementVisible) {
                element.classList.add('active');
            }
        });
    }
    
    window.addEventListener('scroll', revealOnScroll);
    revealOnScroll(); // Initial check
    
    // Gallery filtering
    const filterButtons = document.querySelectorAll('.filter-button');
    const galleryItems = document.querySelectorAll('.gallery-item');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            const filterValue = this.getAttribute('data-filter');
            
            galleryItems.forEach(item => {
                if (filterValue === 'all' || item.classList.contains(filterValue)) {
                    item.style.display = 'block';
                    setTimeout(() => item.classList.add('active'), 200);
                } else {
                    item.classList.remove('active');
                    item.style.display = 'none';
                }
            });
        });
    });
    
    // Testimonial slider (basic version)
    const testimonialCards = document.querySelectorAll('.testimonial-card');
    let currentTestimonial = 0;
    
    function showCurrentTestimonial() {
        testimonialCards.forEach((card, index) => {
            if (window.innerWidth > 992) {
                card.style.display = 'block'; // Desktop: show all
            } else {
                card.style.display = index === currentTestimonial ? 'block' : 'none'; // Mobile: one at a time
            }
        });
    }
    
    // Auto-slide for mobile
    let testimonialInterval = setInterval(() => {
        if (window.innerWidth <= 992) {
            currentTestimonial = (currentTestimonial + 1) % testimonialCards.length;
            showCurrentTestimonial();
        }
    }, 5000);
    
    // On load and on resize
    showCurrentTestimonial();
    window.addEventListener('resize', showCurrentTestimonial);
});
