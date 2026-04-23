/**
 * Aursikho — Main JavaScript
 * Handles navbar scroll, animations, and quiz interactions.
 */

// Navbar scroll effect
window.addEventListener('scroll', () => {
    const navbar = document.getElementById('mainNavbar');
    if (navbar) {
        navbar.classList.toggle('scrolled', window.scrollY > 20);
    }
});

// Auto-dismiss flash messages after 5s
document.addEventListener('DOMContentLoaded', () => {
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            const btn = alert.querySelector('.btn-close');
            if (btn) btn.click();
        }, 5000);
    });
});

// Animate stat numbers on scroll
const observerOptions = { threshold: 0.5 };
const statObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const el = entry.target;
            const target = parseInt(el.getAttribute('data-count')) || 0;
            animateCount(el, 0, target, 1200);
            statObserver.unobserve(el);
        }
    });
}, observerOptions);

document.querySelectorAll('.stat-number[data-count]').forEach(el => {
    statObserver.observe(el);
});

function animateCount(el, start, end, duration) {
    const range = end - start;
    if (range === 0) return;
    const increment = Math.ceil(range / (duration / 16));
    let current = start;
    const timer = setInterval(() => {
        current += increment;
        if (current >= end) {
            current = end;
            clearInterval(timer);
        }
        el.textContent = current;
    }, 16);
}
