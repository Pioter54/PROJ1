// ---- MOTYW CIEMNY/JASNY ----
const themeButton = document.getElementById('theme-button');
const body = document.body;

function applyTheme() {
  if (localStorage.getItem('theme') === 'dark') {
    body.classList.add('dark-theme');
    themeButton.textContent = '☀️';
  } else {
    body.classList.remove('dark-theme');
    themeButton.textContent = '🌙';
  }
}
applyTheme();
themeButton?.addEventListener('click', () => {
  body.classList.toggle('dark-theme');
  const newTheme = body.classList.contains('dark-theme') ? 'dark' : 'light';
  localStorage.setItem('theme', newTheme);
  themeButton.textContent = newTheme === 'dark' ? '☀️' : '🌙';
});

// ---- CZAT I TERRAFORM ----
const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const terraformModalEl = document.getElementById('terraformModal');
const generateButton = document.getElementById('generate-tf');

function appendMessage(content, sender) {
  const wrapper = document.createElement('div');
  wrapper.classList.add('message', sender === 'user' ? 'user-message' : 'bot-message');
  wrapper.textContent = content;
  chatBox?.appendChild(wrapper);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function sendMessage() {
  const message = userInput?.value.trim();
  if (!message) return;
  appendMessage(message, 'user');
  userInput.value = '';

  fetch('/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message })
  })
    .then(r => r.json())
    .then(data => {
      if (data.response) {
        appendMessage(data.response, 'bot');
        return;
      }

      const { type, params } = data;
      generateDynamicForm(type, params);
      const modal = new bootstrap.Modal(terraformModalEl);
      modal.show();
    })
    .catch(err => {
      console.error(err);
      appendMessage('Wystąpił błąd sieci – spróbuj ponownie.', 'bot');
    });
}

function generateDynamicForm(type, params) {
  const form = document.getElementById('terraform-form');
  if (!form) return;

  form.innerHTML = '';
  form.dataset.type = type;

  for (const [key, value] of Object.entries(params)) {
    const field = document.createElement('div');
    field.className = 'mb-3';
    field.innerHTML = `
      <label for="input-${key}" class="form-label">${key}</label>
      <input type="text" class="form-control" id="input-${key}" name="${key}" value="${value || ''}">
    `;
    form.appendChild(field);
  }
}

generateButton?.addEventListener('click', () => {
  const form = document.getElementById('terraform-form');
  const formData = {};
  const type = form.dataset.type;

  Array.from(form.elements).forEach(el => {
    if (el.name) formData[el.name] = el.value;
  });

  fetch('/generate_tf', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ type, params: formData })
  })
    .then(r => r.json())
    .then(data => {
      appendMessage("Wygenerowano:\n" + data.result, 'bot');
      bootstrap.Modal.getInstance(terraformModalEl).hide();
    })
    .catch(err => {
      console.error(err);
      appendMessage("Błąd podczas generowania pliku Terraform.", 'bot');
    });
});

sendButton?.addEventListener('click', sendMessage);
userInput?.addEventListener('keydown', e => {
  if (e.key === 'Enter') sendMessage();
});

// ---- AKTYWACJA PROJEKTU ----
function toggleProjectActive(projectId) {
  fetch(`/toggle_project/${projectId}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ toggle: true })
  })
    .then(response => {
      if (!response.ok) {
        alert('Nie udało się zmienić statusu projektu.');
        return;
      }

      document.querySelectorAll('.project-switch').forEach(sw => {
        const currentId = parseInt(sw.getAttribute('onchange')?.match(/\d+/)[0]);
        sw.checked = (currentId === projectId);
      });
    })
    .catch(err => {
      console.error("Błąd połączenia z toggle_project:", err);
    });
}
