// explore.js
document.querySelectorAll('.category-card').forEach(card => {
    card.addEventListener('click', () => {
        const category = card.dataset.category;
        document.querySelector('.categories-container').style.display = 'none';
        document.querySelector('.category-items-section').style.display = 'block';
        document.getElementById('selected-category-title').textContent = card.querySelector('h3').textContent;
        // Fetch items via AJAX
        fetch(`/search/?category=${category}`)
            .then(response => response.json())
            .then(data => {
                const itemsGrid = document.getElementById('category-items');
                itemsGrid.innerHTML = data.listings.map(item => `
                    <div class="item-card">
                        <img src="${item.image || 'https://via.placeholder.com/150'}" alt="${item.title}">
                        <h3>${item.title}</h3>
                        <p>$${item.price}</p>
                    </div>
                `).join('');
            });
    });
});

document.querySelector('.back-to-categories').addEventListener('click', () => {
    document.querySelector('.categories-container').style.display = 'block';
    document.querySelector('.category-items-section').style.display = 'none';
});