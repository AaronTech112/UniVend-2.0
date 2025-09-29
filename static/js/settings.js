// UnivendApp/static/UnivendApp/js/settings.js
document.addEventListener('DOMContentLoaded', () => {
    // Notifications toggle
    const notificationsToggle = document.getElementById('notificationsToggle');
    if (notificationsToggle) {
        notificationsToggle.addEventListener('change', () => {
            fetch('/update_notifications/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                },
                body: JSON.stringify({
                    email_notifications: notificationsToggle.checked,
                }),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        console.log('Notifications preference updated');
                    } else {
                        console.error('Failed to update notifications');
                        notificationsToggle.checked = !notificationsToggle.checked; // Revert on failure
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    notificationsToggle.checked = !notificationsToggle.checked; // Revert on failure
                });
        });
    }

    // Dark mode toggle (client-side only for demo; persist via backend if needed)
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('change', () => {
            document.body.classList.toggle('dark-mode', darkModeToggle.checked);
        });
    }
});