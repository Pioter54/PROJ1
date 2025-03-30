// script.js
const themeButton = document.getElementById('theme-button');
const body = document.body;
const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const jsonReview = document.getElementById('json-review');
const jsonEditor = document.getElementById('json-editor');
const approveButton = document.getElementById('approve-button');

themeButton.addEventListener('click', () => {
    body.classList.toggle('dark-theme');
    themeButton.textContent = body.classList.contains('dark-theme') ? '☀️' : '🌙';
});

function appendMessage(content, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender === 'user' ? 'user-message' : 'bot-message');
    messageDiv.textContent = content;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function sendMessage() {
    const message = userInput.value.trim();
    if (message) {
        appendMessage(message, 'user');
        userInput.value = '';
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.json_code) {
                jsonEditor.value = data.json_code;
                const modal = new bootstrap.Modal(document.getElementById('jsonModal'));
                modal.show();
            } else {
                appendMessage("Nie udało się wygenerować kodu JSON.", 'bot');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            appendMessage('Wystąpił błąd. Spróbuj ponownie.', 'bot');
        });
    }
}

sendButton.addEventListener('click', sendMessage);

userInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

// Obsługa zatwierdzenia JSON przez użytkownika
approveButton.addEventListener('click', () => {
    const approvedJson = jsonEditor.value.trim();
    if (approvedJson) {
        fetch('/approve_json', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ json_code: approvedJson }),
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('terraform-output').textContent = data.response;
            const terraformModal = new bootstrap.Modal(document.getElementById('terraformModal'));
            terraformModal.show();
            appendMessage(data.terraform_result, 'bot');
            const modalElement = document.getElementById('jsonModal');
            const modalInstance = bootstrap.Modal.getInstance(modalElement);
            modalInstance.hide();
        })
        .catch(error => {
            console.error('Error:', error);
            appendMessage('Wystąpił błąd podczas zatwierdzania JSON.', 'bot');
        });
    }
});

