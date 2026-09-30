document.addEventListener('DOMContentLoaded', function () {
    const dataElement = document.querySelector('#glossary-match-data');
    const board = document.querySelector('#match-board');
    if (!dataElement || !board) return;

    const terms = JSON.parse(dataElement.textContent);
    const scoreElement = document.querySelector('#match-score');
    const streakElement = document.querySelector('#match-streak');
    const movesElement = document.querySelector('#match-moves');
    const timerElement = document.querySelector('#match-timer');
    const messageElement = document.querySelector('#match-message');
    const resultElement = document.querySelector('#match-result');
    const resultText = document.querySelector('#match-result-text');
    const restartButtons = [document.querySelector('#match-restart'), document.querySelector('#match-play-again')];

    let selectedCard = null;
    let matchedCount = 0;
    let score = 0;
    let streak = 0;
    let moves = 0;
    let seconds = 0;
    let timer = null;
    let locked = false;

    function shuffle(items) {
        return [...items].sort(() => Math.random() - 0.5);
    }

    function updateStatus() {
        scoreElement.textContent = score;
        streakElement.textContent = streak;
        movesElement.textContent = moves;
        const minutes = String(Math.floor(seconds / 60)).padStart(2, '0');
        const remainingSeconds = String(seconds % 60).padStart(2, '0');
        timerElement.textContent = `${minutes}:${remainingSeconds}`;
    }

    function startTimer() {
        if (timer) return;
        timer = window.setInterval(function () {
            seconds += 1;
            updateStatus();
        }, 1000);
    }

    function createCard(type, term) {
        const card = document.createElement('button');
        card.type = 'button';
        card.className = `match-card match-card-${type}`;
        card.dataset.termId = term.id;
        card.dataset.type = type;
        card.innerHTML = `<span class="match-card-label">${type === 'term' ? 'Kavram' : 'Tanım'}</span><span class="match-card-content">${type === 'term' ? term.title : term.definition}</span>`;
        card.addEventListener('click', function () {
            chooseCard(card);
        });
        return card;
    }

    function chooseCard(card) {
        if (locked || card.disabled || card === selectedCard) return;
        startTimer();
        card.classList.add('selected');
        if (!selectedCard) {
            selectedCard = card;
            messageElement.textContent = 'Şimdi eşleşen kartı bul.';
            return;
        }

        moves += 1;
        const isMatch = selectedCard.dataset.termId === card.dataset.termId && selectedCard.dataset.type !== card.dataset.type;
        if (isMatch) {
            selectedCard.classList.add('matched');
            card.classList.add('matched');
            selectedCard.disabled = true;
            card.disabled = true;
            matchedCount += 1;
            streak += 1;
            score += 100 + (streak - 1) * 25;
            messageElement.textContent = streak > 1 ? `${streak} doğru eşleşme üst üste. Harika gidiyorsun.` : 'Doğru eşleşme. Bir sonraki çifti bul.';
            selectedCard = null;
            updateStatus();
            if (matchedCount === terms.length) finishGame();
            return;
        }

        locked = true;
        streak = 0;
        messageElement.textContent = 'Bu iki kart eşleşmedi. Tanımı dikkatle oku ve tekrar dene.';
        window.setTimeout(function () {
            selectedCard.classList.remove('selected');
            card.classList.remove('selected');
            selectedCard = null;
            locked = false;
            updateStatus();
        }, 750);
    }

    function finishGame() {
        window.clearInterval(timer);
        timer = null;
        resultText.textContent = `${terms.length} çifti ${moves} hamlede, ${timerElement.textContent} içinde tamamladın. Toplam puanın: ${score}. Sözlükteki bir terimi açıp öğrendiğin kavramı gerçek bir proje fikrine dönüştürmeyi dene.`;
        resultElement.hidden = false;
        messageElement.textContent = 'Tur tamamlandı. İstersen yeni bir kart dizilimiyle tekrar oynayabilirsin.';
    }

    function startGame() {
        window.clearInterval(timer);
        timer = null;
        selectedCard = null;
        matchedCount = 0;
        score = 0;
        streak = 0;
        moves = 0;
        seconds = 0;
        locked = false;
        resultElement.hidden = true;
        messageElement.textContent = 'Önce bir kavram, ardından ona ait tanımı seç.';
        board.replaceChildren();
        const cards = shuffle(terms.flatMap(function (term) {
            return [createCard('term', term), createCard('definition', term)];
        }));
        cards.forEach(function (card) {
            board.appendChild(card);
        });
        updateStatus();
    }

    restartButtons.forEach(function (button) {
        if (button) button.addEventListener('click', startGame);
    });

    startGame();
});
