(() => {
    const cards = [...document.querySelectorAll('.mission-card')];
    const summary = document.querySelector('.mission-score');
    const summaryButton = document.querySelector('#mission-summary-button');
    if (!cards.length || !summary || !summaryButton) return;

    const storageKey = 'iklimkiti-digital-missions-v2';
    const correctAnswers = {
        kuraklik: 'b',
        'gida-guvenligi': 'a',
        'israfi-onle': 'a',
    };
    const explanations = {
        kuraklik: 'Gıda ve su kararlarında yerel koşulları, güvenilir iklim verisini ve su verimliliğini birlikte değerlendirmek dayanıklılığı artırır.',
        'gida-guvenligi': 'Güvenli saklamada ürün etiketi ve resmî gıda güvenliği yönlendirmeleri esastır. Şüphedeysen ürünü tüketme; güvenilir bir yetişkine danış.',
        'israfi-onle': 'Evdeki gıdayı kontrol etmek ve planlı alışveriş yapmak ihtiyaç fazlasını önlemeye yardımcı olur; saklama koşullarını ürün etiketinden kontrol et.',
    };

    let progress = { first: {}, latest: {} };
    try {
        const stored = JSON.parse(localStorage.getItem(storageKey) || 'null');
        if (stored && typeof stored === 'object' && !Array.isArray(stored)) {
            progress = {
                first: stored.first && typeof stored.first === 'object' ? stored.first : {},
                latest: stored.latest && typeof stored.latest === 'object' ? stored.latest : {},
            };
        }
    } catch (_) {
        progress = {};
    }

    const save = () => {
        try { localStorage.setItem(storageKey, JSON.stringify(progress)); } catch (_) { /* Keep the activity usable when storage is unavailable. */ }
    };

    const updateSummary = () => {
        const answered = Object.keys(progress.latest).filter(key => Object.hasOwn(correctAnswers, key));
        const firstAnswered = Object.keys(progress.first).filter(key => Object.hasOwn(correctAnswers, key));
        const firstCorrect = firstAnswered.filter(key => progress.first[key] === correctAnswers[key]).length;
        const latestCorrect = answered.filter(key => progress.latest[key] === correctAnswers[key]).length;
        if (!answered.length) {
            summary.textContent = 'Henüz görev tamamlamadın. Bir senaryoda kararını değerlendir.';
        } else if (answered.length < cards.length) {
            summary.textContent = `${answered.length}/${cards.length} görev tamamlandı · son denemende ${latestCorrect} doğru karar. Kaldığın yerden devam edebilirsin.`;
        } else {
            summary.textContent = `İlk tur: ${firstCorrect}/${firstAnswered.length} · son deneme: ${latestCorrect}/${cards.length}. Bu kişisel bir tekrar ölçümüdür; bilimsel ölçek veya gerçek karbon/su tasarrufu iddiası değildir.`;
        }
    };

    cards.forEach(card => {
        const mission = card.dataset.mission;
        const form = card.querySelector('form');
        const feedback = card.querySelector('.mission-feedback');

        const completeMission = selectedValue => {
            const selectedAnswer = form.querySelector(`input[type="radio"][value="${selectedValue}"]`);
            if (selectedAnswer) selectedAnswer.checked = true;
            form.querySelectorAll('input, button').forEach(control => {
                control.disabled = true;
            });
            feedback.hidden = false;
            feedback.className = 'mission-feedback is-correct';
            feedback.textContent = `Güçlü karar. ${explanations[mission]}`;
            card.classList.add('mission-complete');
        };

        if (progress.latest[mission] === correctAnswers[mission]) {
            completeMission(progress.latest[mission]);
        }

        form.addEventListener('submit', event => {
            event.preventDefault();
            if (card.classList.contains('mission-complete')) return;
            const selected = form.querySelector('input[type="radio"]:checked');
            if (!selected) {
                feedback.hidden = false;
                feedback.className = 'mission-feedback is-prompt';
                feedback.textContent = 'Önce bir seçenek belirle.';
                return;
            }

            const isCorrect = selected.value === correctAnswers[mission];
            if (!Object.hasOwn(progress.first, mission)) progress.first[mission] = selected.value;
            progress.latest[mission] = selected.value;
            save();
            feedback.hidden = false;
            feedback.className = `mission-feedback ${isCorrect ? 'is-correct' : 'is-review'}`;
            feedback.textContent = `${isCorrect ? 'Güçlü karar.' : 'Bir kez daha düşün.'} ${explanations[mission]}`;
            if (isCorrect) {
                completeMission(selected.value);
                if (typeof window.celebrateSuccess === 'function') {
                    window.celebrateSuccess('Doğru karar! Görev tamamlandı 🎉');
                }
            }
            updateSummary();
        });
    });

    summaryButton.addEventListener('click', updateSummary);
    updateSummary();
})();
