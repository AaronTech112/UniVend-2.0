document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM fully loaded');

    const form = document.getElementById('listingForm');
    if (!form) {
        console.error('Error: Form element with ID "listingForm" not found');
        return;
    }

    // Character count for title and description
    document.querySelectorAll('input[name="title"], textarea[name="description"]').forEach(input => {
        input.addEventListener('input', () => {
            const count = input.value.length;
            const max = input.getAttribute('maxlength');
            const counter = input.nextElementSibling;
            if (counter && counter.classList.contains('character-count')) {
                counter.textContent = `${count}/${max}`;
            }
        });
    });

    // Show/hide condition field based on listing type
    const conditionGroup = document.getElementById('conditionGroup');
    const conditionSelect = document.getElementById('conditionSelect');
    const listingTypeInputs = document.querySelectorAll('input[name="listing_type"]');

    function updateConditionField() {
        const listingType = document.querySelector('input[name="listing_type"]:checked')?.value;
        if (listingType === 'product') {
            conditionGroup.style.display = 'block';
            conditionSelect.setAttribute('required', 'required');
        } else {
            conditionGroup.style.display = 'none';
            conditionSelect.removeAttribute('required');
            conditionSelect.value = ''; // Reset condition for services
        }
    }

    listingTypeInputs.forEach(input => {
        input.addEventListener('change', updateConditionField);
    });

    // Initialize condition field visibility
    updateConditionField();
});