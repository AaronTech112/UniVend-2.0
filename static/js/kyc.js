// kyc.js
const forms = document.querySelectorAll('.step-form');
const progressBar = document.querySelector('.progress-bar');
const steps = document.querySelectorAll('.steps-indicator .step');
let currentStep = 0;

function showStep(step) {
    forms.forEach((f, i) => f.classList.toggle('active', i === step));
    steps.forEach((s, i) => s.classList.toggle('active', i <= step));
    progressBar.style.width = `${(step + 1) * 25}%`;
    progressBar.setAttribute('aria-valuenow', (step + 1) * 25);
}

document.querySelectorAll('.btn-next').forEach(btn => {
    btn.addEventListener('click', () => {
        const form = btn.closest('form');
        if (form.checkValidity()) {
            form.submit();
        } else {
            form.reportValidity();
        }
    });
});

document.querySelectorAll('.btn-back').forEach(btn => {
    btn.addEventListener('click', () => {
        if (currentStep > 0) {
            currentStep--;
            showStep(currentStep);
        }
    });
});

document.querySelectorAll('.upload-area input').forEach(input => {
    input.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                const img = document.createElement('img');
                img.src = e.target.result;
                input.parentElement.innerHTML = '';
                input.parentElement.appendChild(img);
                input.parentElement.appendChild(input);
            };
            reader.readAsDataURL(file);
        }
    });
});

// Initialize
showStep(currentStep);