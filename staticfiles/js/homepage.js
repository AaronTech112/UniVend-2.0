// homepage.js
document.addEventListener('DOMContentLoaded', function() {
    // Category selection
    const categories = document.querySelectorAll('.category');
    categories.forEach(category => {
        category.addEventListener('click', () => {
            categories.forEach(c => c.classList.remove('active'));
            category.classList.add('active');
        });
    });

    // Bottom navigation
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            navItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');
        });
    });

    // Add button action
    const addButton = document.querySelector('.add-button');
    addButton.addEventListener('click', () => {
        // Add new listing logic here
        console.log('Add new listing');
    });

    // Smooth scroll for horizontal scrolling sections
    const scrollContainers = document.querySelectorAll('.featured-scroll, .categories-scroll');
    scrollContainers.forEach(container => {
        let isDown = false;
        let startX;
        let scrollLeft;

        container.addEventListener('mousedown', (e) => {
            isDown = true;
            container.classList.add('active');
            startX = e.pageX - container.offsetLeft;
            scrollLeft = container.scrollLeft;
        });

        container.addEventListener('mouseleave', () => {
            isDown = false;
            container.classList.remove('active');
        });

        container.addEventListener('mouseup', () => {
            isDown = false;
            container.classList.remove('active');
        });

        container.addEventListener('mousemove', (e) => {
            if (!isDown) return;
            e.preventDefault();
            const x = e.pageX - container.offsetLeft;
            const walk = (x - startX) * 2;
            container.scrollLeft = scrollLeft - walk;
        });
    });
});