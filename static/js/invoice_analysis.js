document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('#invoice-form');
    const eInvoice = document.querySelector('#e-invoice');
    const eInvoiceFields = document.querySelector('#e-invoice-fields');
    const status = document.querySelector('#invoice-status');
    const results = document.querySelector('#analysis-results');
    if (!form || !eInvoice || !eInvoiceFields || !status || !results) return;

    eInvoice.addEventListener('change', function () {
        eInvoiceFields.hidden = !eInvoice.checked;
        eInvoiceFields.querySelectorAll('input').forEach(function (input) {
            input.required = eInvoice.checked;
        });
        form.querySelectorAll('input[type="file"]').forEach(function (input) {
            input.required = !eInvoice.checked;
        });
        const uploadGrid = form.querySelector('.bill-upload-grid');
        const uploadNote = uploadGrid.previousElementSibling;
        uploadGrid.hidden = eInvoice.checked;
        uploadNote.hidden = eInvoice.checked;
    });

    form.querySelectorAll('input[type="file"]').forEach(function (input) {
        input.addEventListener('change', function () {
            const label = input.closest('.bill-upload');
            const name = label.querySelector('.file-name');
            name.textContent = input.files[0] ? input.files[0].name : 'Dosya seçilmedi';
            label.classList.toggle('has-file', Boolean(input.files[0]));
        });
    });

    form.addEventListener('submit', async function (event) {
        event.preventDefault();
        status.className = 'form-status';
        status.textContent = 'Faturalar inceleniyor...';
        results.hidden = true;
        try {
            const response = await fetch('/api/fatura-analizi/', {
                method: 'POST',
                headers: {'X-CSRFToken': document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1] || ''},
                body: new FormData(form),
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Analiz tamamlanamadı.');
            status.className = 'form-status success';
            status.textContent = 'Analiz tamamlandı.';
            results.innerHTML = renderResults(data);
            results.hidden = false;
            results.scrollIntoView({behavior: 'smooth', block: 'start'});
        } catch (error) {
            status.className = 'form-status error';
            status.textContent = error.message;
        }
    });

    function renderResults(data) {
        const messages = data.invoice_messages.map(message => `<li>${escapeHtml(message)}</li>`).join('');
        const recommendations = data.recommendations.map(item => `<li>${escapeHtml(item)}</li>`).join('');
        return `<div class="section-head"><div><p class="eyebrow">3 · Kişisel sonuçların</p><h2>Uygulanabilir karbon planın</h2></div><span class="score-badge">${data.verified_count}/3 doğrulandı</span></div>
            <div class="carbon-summary"><div><strong>${data.carbon} kg</strong><span>Dönem tahmini</span></div><div><strong>${data.per_person_carbon} kg</strong><span>Kişi başına</span></div></div>
            <p class="comparison">${escapeHtml(data.comparison)}</p>
            <div class="target-grid"><div><strong>${data.targets.daily} kg</strong><span>Günlük hedef</span><small>Her gün 1 küçük adım</small></div><div><strong>${data.targets.weekly} kg</strong><span>Haftalık hedef</span><small>Haftalık tüketim kontrolü</small></div><div><strong>${data.targets.monthly} kg</strong><span>Aylık hedef</span><small>Bir sonraki faturada karşılaştır</small></div></div>
            <div class="recommendation-grid"><div class="card"><h3>Bu hafta dene</h3><ul>${recommendations}</ul></div><div class="card"><h3>Görsel kontrolü</h3><ul>${messages}</ul></div></div>`;
    }

    function escapeHtml(value) {
        return String(value).replace(/[&<>"']/g, function (character) {
            return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'}[character];
        });
    }
});
