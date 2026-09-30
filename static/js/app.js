document.addEventListener('DOMContentLoaded', function () {
    const navToggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');
    if (navToggle && navLinks) {
        navToggle.addEventListener('click', function () {
            navLinks.classList.toggle('open');
        });
    }

    const launcher = document.querySelector('.chatbot-launcher');
    const panel = document.querySelector('.chatbot-panel');
    const closeButton = document.querySelector('.close-chat');
    const form = document.querySelector('#chatbot-form');
    const input = document.querySelector('#chatbot-input');
    const body = document.querySelector('#chatbot-body');

    if (launcher && panel) {
        launcher.addEventListener('click', function () {
            panel.classList.toggle('open');
        });
    }

    if (closeButton && panel) {
        closeButton.addEventListener('click', function () {
            panel.classList.remove('open');
        });
    }

    if (form && input && body) {
        form.addEventListener('submit', async function (event) {
            event.preventDefault();
            const value = input.value.trim();
            if (!value) return;
            const userMessage = document.createElement('div');
            userMessage.className = 'message user';
            userMessage.textContent = value;
            body.appendChild(userMessage);
            input.value = '';

            const status = document.createElement('div');
            status.className = 'message bot';
            status.textContent = 'Düşünüyorum...';
            body.appendChild(status);

            try {
                const response = await fetch('/api/chatbot/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-CSRFToken': document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1] || ''},
                    body: new URLSearchParams({ message: value })
                });
                const data = await response.json();
                if (!response.ok) {
                    throw new Error(data.error || 'Hata');
                }
                status.textContent = data.reply;
            } catch (error) {
                status.textContent = 'İklimKiti Asistanı şu anda yanıt veremiyor. Lütfen daha sonra tekrar deneyin veya konu sayfalarındaki güvenilir kaynakları inceleyin.';
            }

            body.scrollTop = body.scrollHeight;
        });
    }
});
