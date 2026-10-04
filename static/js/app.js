window.celebrateSuccess = function (message = 'Harika iş!') {
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const banner = document.createElement('div');
    banner.className = 'success-banner';
    banner.setAttribute('role', 'status');
    banner.textContent = message;
    document.body.appendChild(banner);

    if (!reducedMotion) {
        const colors = ['#19C3B1', '#37D67A', '#F4C95D', '#3A86FF', '#FF6B6B'];
        const fragment = document.createDocumentFragment();
        for (let index = 0; index < 36; index += 1) {
            const piece = document.createElement('span');
            piece.className = 'confetti-piece';
            piece.style.setProperty('--confetti-color', colors[index % colors.length]);
            piece.style.setProperty('--confetti-x', `${(Math.random() - 0.5) * 100}vw`);
            piece.style.setProperty('--confetti-delay', `${Math.random() * 180}ms`);
            piece.style.setProperty('--confetti-rotation', `${Math.random() * 360}deg`);
            fragment.appendChild(piece);
        }
        const confetti = document.createElement('div');
        confetti.className = 'confetti';
        confetti.setAttribute('aria-hidden', 'true');
        confetti.appendChild(fragment);
        document.body.appendChild(confetti);
        window.setTimeout(() => confetti.remove(), 1800);
    }

    window.setTimeout(() => banner.remove(), 2600);
};

function renderBotReply(element, text) {
    const boldPattern = /\*\*(.+?)\*\*/g;
    let lastIndex = 0;
    let match;

    while ((match = boldPattern.exec(text)) !== null) {
        element.appendChild(document.createTextNode(text.slice(lastIndex, match.index)));
        const strong = document.createElement('strong');
        strong.textContent = match[1];
        element.appendChild(strong);
        lastIndex = boldPattern.lastIndex;
    }

    element.appendChild(document.createTextNode(text.slice(lastIndex)));
}

document.addEventListener('DOMContentLoaded', function () {
    const usernameInput = document.querySelector('.form-card input[name="username"]');
    const cultureEgg = document.querySelector('#culture-egg');
    if (usernameInput && cultureEgg) {
        const updateCultureEgg = function () {
            cultureEgg.hidden = usernameInput.value.trim().toLocaleLowerCase('tr-TR') !== 'yahu';
        };
        usernameInput.addEventListener('input', updateCultureEgg);
        updateCultureEgg();
    }

    const navToggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');
    if (navToggle && navLinks) {
        const closeMenu = function (restoreFocus = false) {
            navLinks.classList.remove('open');
            navToggle.classList.remove('is-open');
            navToggle.setAttribute('aria-expanded', 'false');
            navToggle.setAttribute('aria-label', 'Menüyü aç');
            if (restoreFocus) navToggle.focus();
        };

        navToggle.addEventListener('click', function () {
            const isOpen = !navLinks.classList.contains('open');
            navLinks.classList.toggle('open', isOpen);
            navToggle.classList.toggle('is-open', isOpen);
            navToggle.setAttribute('aria-expanded', String(isOpen));
            navToggle.setAttribute('aria-label', isOpen ? 'Menüyü kapat' : 'Menüyü aç');
        });

        navLinks.querySelectorAll('a').forEach(function (link) {
            const linkPath = new URL(link.href, window.location.href).pathname.replace(/\/+$/, '') || '/';
            const currentPath = window.location.pathname.replace(/\/+$/, '') || '/';
            if (linkPath === currentPath) link.setAttribute('aria-current', 'page');
            link.addEventListener('click', function () {
                closeMenu();
            });

            if (window.matchMedia('(hover: hover) and (pointer: fine) and (min-width: 761px)').matches) {
                link.addEventListener('pointermove', function (event) {
                    if (event.pointerType !== 'mouse') return;
                    const bounds = link.getBoundingClientRect();
                    const x = (event.clientX - bounds.left) / bounds.width;
                    const y = (event.clientY - bounds.top) / bounds.height;
                    link.style.setProperty('--pointer-x', `${x * 100}%`);
                    link.style.setProperty('--pointer-y', `${y * 100}%`);
                    link.style.setProperty('--link-shift-x', `${(x - 0.5) * 5}px`);
                    link.style.setProperty('--link-shift-y', `${(y - 0.5) * 4 - 1}px`);
                });
                link.addEventListener('pointerleave', function () {
                    link.style.removeProperty('--pointer-x');
                    link.style.removeProperty('--pointer-y');
                    link.style.removeProperty('--link-shift-x');
                    link.style.removeProperty('--link-shift-y');
                });
            }
        });

        document.addEventListener('click', function (event) {
            if (navLinks.classList.contains('open')
                && !navLinks.contains(event.target)
                && !navToggle.contains(event.target)) {
                closeMenu();
            }
        });

        document.addEventListener('keydown', function (event) {
            if (event.key === 'Escape' && navLinks.classList.contains('open')) {
                closeMenu(true);
            }
        });

        window.matchMedia('(min-width: 1101px)').addEventListener('change', function (event) {
            if (event.matches) closeMenu();
        });
    }

    const brand = document.querySelector('.brand');
    if (brand && window.matchMedia('(hover: hover) and (pointer: fine)').matches
        && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        brand.addEventListener('pointermove', function (event) {
            if (event.pointerType !== 'mouse') return;
            const bounds = brand.getBoundingClientRect();
            const x = (event.clientX - bounds.left) / bounds.width - 0.5;
            const y = (event.clientY - bounds.top) / bounds.height - 0.5;
            brand.style.setProperty('--brand-tilt-x', `${-y * 12}deg`);
            brand.style.setProperty('--brand-tilt-y', `${x * 12}deg`);
        });
        brand.addEventListener('pointerleave', function () {
            brand.style.setProperty('--brand-tilt-x', '0deg');
            brand.style.setProperty('--brand-tilt-y', '0deg');
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
        const requestAssistantReply = async function (value, retriesLeft = 5) {
            try {
                const response = await fetch('/api/chatbot/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'X-CSRFToken': document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1] || ''
                    },
                    body: new URLSearchParams({ message: value })
                });
                const data = await response.json();
                if (!response.ok) {
                    throw new Error(data.error || 'Hata');
                }
                return data.reply;
            } catch (error) {
                if (retriesLeft > 0) {
                    await new Promise(resolve => window.setTimeout(resolve, 700 * (6 - retriesLeft)));
                    return requestAssistantReply(value, retriesLeft - 1);
                }
                throw error;
            }
        };

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
            status.className = 'message bot typing-indicator';
            status.setAttribute('role', 'status');
            status.setAttribute('aria-label', 'Asistan yanıt yazıyor');
            status.appendChild(document.createTextNode('Yanıt hazırlanıyor'));
            for (let index = 0; index < 3; index += 1) {
                const dot = document.createElement('span');
                dot.className = 'typing-dot';
                dot.setAttribute('aria-hidden', 'true');
                status.appendChild(dot);
            }
            body.appendChild(status);
            body.scrollTop = body.scrollHeight;

            try {
                const reply = await requestAssistantReply(value, 5);
                status.classList.remove('typing-indicator');
                status.removeAttribute('aria-label');
                status.removeAttribute('role');
                status.textContent = '';
                renderBotReply(status, reply);
            } catch (error) {
                status.classList.remove('typing-indicator');
                status.removeAttribute('aria-label');
                status.removeAttribute('role');
                status.textContent = 'İklim Tabağım Asistanı şu anda yanıt veremiyor. Lütfen daha sonra tekrar deneyin veya konu sayfalarındaki güvenilir kaynakları inceleyin.';
            }

            body.scrollTop = body.scrollHeight;
        });
    }
});
