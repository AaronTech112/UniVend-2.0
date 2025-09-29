// chat-list.js
document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const filter = btn.dataset.filter;
        document.querySelectorAll('.chat-item').forEach(item => {
            if (filter === 'all') {
                item.style.display = 'flex';
            } else if (filter === 'unread' && item.classList.contains('unread')) {
                item.style.display = 'flex';
            } else if (filter === 'active-orders' && item.classList.contains('active-order')) {
                item.style.display = 'flex';
            } else {
                item.style.display = 'none';
            }
        });
    });
});

document.querySelectorAll('.chat-item').forEach(item => {
    item.addEventListener('click', () => {
        window.location.href = `/chat/${item.dataset.chatId}/`;
    });
});