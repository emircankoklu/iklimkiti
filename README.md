# İklim Tabağım
İklim Tabağım: Gıda güvenliği, iklim eğitimi ve etkileşimli öğrenme platformu.

## Fatura ve karbon analizi

Giriş yapmış kullanıcılar `/fatura-analizi/` sayfasından elektrik, doğal gaz ve su faturalarının
fotoğraflarını aynı anda yükleyebilir. Sayfa; kat konumu, hane kişi sayısı ve duş sıklığını da
hesaba katarak dönemsel karbon tahmini, günlük/haftalık/aylık hedefler ve uygulanabilir öneriler
üretir. `GEMINI_API_KEY` tanımlıysa görseller Gemini ile fatura türü açısından doğrulanır ve
tüketim değeri çıkarılır. Alternatif olarak OpenAI uyumlu NVIDIA NIM görsel modeli kullanılabilir.
Anahtar tanımlı değilse yüklemeler güvenli bir şekilde “manuel kontrol” olarak işaretlenir;
e-fatura seçeneğindeki tüketim değerleriyle analiz sürdürülebilir.

### AI sağlayıcısı yapılandırması

Admin ana sayfasındaki **AI sağlayıcıları ve API anahtarları** sekmesi; aktif sağlayıcıyı,
modeli, endpoint'i ve anahtarın tanımlı olup olmadığını maskeli biçimde gösterir. Anahtarlar
güvenlik nedeniyle veritabanına yazılmaz. Proje kökündeki `.env` dosyasında aşağıdaki değerler
kullanılır:

```env
INVOICE_AI_PROVIDER=gemini
GEMINI_API_KEY=...
GEMINI_MODEL=gemini-2.0-flash
```

NVIDIA NIM kullanmak için:

```env
INVOICE_AI_PROVIDER=nvidia
NVIDIA_API_KEY=...
NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1
NVIDIA_INVOICE_MODEL=meta/llama-3.2-90b-vision-instruct
```

NVIDIA tarafında seçilen modelin görsel girdi desteklediğinden emin olun. `.env` değiştikten
sonra Django uygulamasını yeniden başlatmak gerekir. API anahtarlarını git'e göndermeyin.

Desteklenen görseller JPG, PNG ve WEBP formatlarında, dosya başına en fazla 8 MB olmalıdır.
Fotoğraflar kalıcı olarak saklanmaz.
