// product-detail.js
const images = document.querySelectorAll('.slider-container img');
const dots = document.querySelectorAll('.slider-dots .dot');
let currentImage = 0;

function showImage(index) {
    images.forEach((img, i) => img.classList.toggle('active', i === index));
    dots.forEach((dot, i) => dot.classList.toggle('active', i === index));
}

dots.forEach((dot, i) => {
    dot.addEventListener('click', () => {
        currentImage = i;
        showImage(currentImage);
    });
});

// Report modal
const reportModal = document.getElementById('reportModal');
document.querySelector('.share-button').addEventListener('click', () => {
    reportModal.style.display = 'block';
});

document.querySelector('.cancel-button').addEventListener('click', () => {
    reportModal.style.display = 'none';
});

// Show Contact functionality
const showContactBtn = document.querySelector('#show-contact-btn');

if (showContactBtn) {
    showContactBtn.addEventListener('click', () => {
        const phoneNumber = showContactBtn.getAttribute('data-phone');
        if (phoneNumber) {
            showContactBtn.textContent = phoneNumber;
        } else {
            showContactBtn.textContent = 'No phone number available';
        }
        showContactBtn.disabled = true;
    });
}

// Helper function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}