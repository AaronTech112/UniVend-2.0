// UnivendApp/static/UnivendApp/js/profile.js
document.addEventListener('DOMContentLoaded', () => {
    // Tab switching (for profile page)
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabPanes = document.querySelectorAll('.tab-pane');

    if (tabButtons && tabPanes) {
        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                tabButtons.forEach(btn => btn.classList.remove('active'));
                tabPanes.forEach(pane => pane.classList.remove('active'));

                button.classList.add('active');
                const tabId = button.getAttribute('data-tab');
                document.getElementById(tabId).classList.add('active');
            });
        });
    }

    // Avatar preview (for edit profile page)
    const profilePicInput = document.querySelector('#id_profile_picture');
    const avatarPreview = document.getElementById('avatarPreview');
    const changeAvatarBtn = document.querySelector('.change-avatar');

    if (changeAvatarBtn && profilePicInput && avatarPreview) {
        changeAvatarBtn.addEventListener('click', () => {
            profilePicInput.click();
        });

        profilePicInput.addEventListener('change', () => {
            const file = profilePicInput.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    avatarPreview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // Edit listing button (for profile page)
    const editListingButtons = document.querySelectorAll('.edit-listing');
    if (editListingButtons) {
        editListingButtons.forEach(button => {
            button.addEventListener('click', () => {
                const listingId = button.getAttribute('data-listing-id');
                alert(`Edit listing ID: ${listingId}`);
                // TODO: Implement edit listing functionality
            });
        });
    }
});