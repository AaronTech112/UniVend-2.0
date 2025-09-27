// chat-detail.js
const messageInput = document.getElementById('messageInput');
const sendButton = document.querySelector('.send-button');
const attachmentButton = document.querySelector('.attachment-button');
const attachmentMenu = document.getElementById('attachmentMenu');
const messageImage = document.getElementById('messageImage');

messageInput.addEventListener('input', () => {
    sendButton.disabled = !messageInput.value.trim();
});

attachmentButton.addEventListener('click', () => {
    attachmentMenu.style.display = attachmentMenu.style.display === 'block' ? 'none' : 'block';
});

document.querySelectorAll('.attachment-option').forEach(option => {
    option.addEventListener('click', () => {
        if (option.textContent.includes('Gallery') || option.textContent.includes('Camera')) {
            messageImage.click();
        }
        attachmentMenu.style.display = 'none';
    });
});

messageImage.addEventListener('change', () => {
    if (messageImage.files[0]) {
        document.getElementById('messageForm').submit();
    }
});

// Auto-scroll to bottom
const chatMessages = document.getElementById('chatMessages');
chatMessages.scrollTop = chatMessages.scrollHeight;