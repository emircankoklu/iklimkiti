from django.core.management.base import BaseCommand

from core.models import GuideSection, IdeathonGuide


class Command(BaseCommand):
    help = 'Create or update the COP31 ideathon guide content.'

    def handle(self, *args, **options):
        guide, _ = IdeathonGuide.objects.update_or_create(
            pk=1,
            defaults={
                'title': 'İklim Karar Laboratuvarı: QR’dan dijital öğrenmeye',
                'subtitle': 'Fiziksel okul altyapısı gerektirmeyen, web sitesi üzerinden yürütülen 30 günlük öğrenci pilotu',
                'introduction': "Projemiz yemekhane, kantin, tartım veya okulda fiziksel uygulama gerektirmiyor. Öğrenciler QR kodla siteye ulaşır; iklim ve gıda güvenliği senaryolarında karar verir, geri bildirim alır ve kendi cihazlarında öğrenme özetini görür. Ayırt edici yaklaşım, öğrencilerin yazdığı kaynaklı senaryoların farklı seçimlerin sonuçlarını gösteren dijital karar laboratuvarına dönüşmesidir. Yanıtlar sunucuya gönderilmez; gerçek çevresel tasarruf iddiası yerine ölçülebilen öğrenme sonucu raporlanır.",
                'source_url': 'https://meslegimhayatim.meb.gov.tr/cop31/Yarisma_Sartnamesi_ve_Basvuru_Rehberi.pdf',
                'is_published': True,
            },
        )
        sections = [
            ('1 · Gıda güvenliği ve iklim sorununu kaynaklarla temellendir', 'Problem ve kanıt · 30 puan', 30,
             'Yemekhane verisi varsaymayın. Proje problemini resmî açık veriler, doğrulanabilir kaynaklar ve site senaryolarındaki ilk tur/son deneme öğrenme ölçümüyle çerçeveleyin. Site kaynakçasındaki her iklim, su veya gıda güvenliği iddiasına kaynak ve tarih ekleyin. Anket kullanılacaksa gönüllü ve anonim tutun; elde edilmemiş saha verisini varmış gibi sunmayın.',
             'Hangi güvenilir kaynak ve hangi site içi öğrenme göstergesi problem tanımımızı destekliyor?'),
            ('2 · Öğrenci üretimi dijital senaryolar yaz', 'Öğrenci araştırması', 0,
             'Ekipler kuraklık ve su verimliliği, sıcak havada güvenli gıda seçimi, planlı alışveriş ve güvenli saklama üzerine kısa karar senaryoları yazar. Her senaryo güvenilir kaynakla doğrulanır; yanlış seçenekler utandırmadan nedenini açıklar. Böylece öğrenci hazır bilgi tüketmek yerine araştırır, yazar ve içerik üretir.',
             'Bir öğrencinin yazdığı senaryoda hangi kaynağa dayandığı ve hangi öğrenme kazanımını hedeflediği görünür mü?'),
            ('3 · “İklim Karar Laboratuvarı”nı QR’dan açılır hâle getir', 'Özgün çözüm · 25 puan', 25,
             'Her kısa görev bir durum, öğrencinin seçebileceği yollar ve seçimin sonucunu açıklayan geri bildirim içerir. QR kodlar ileride doğrudan ilgili göreve bağlanabilir; şu an görevler site bağlantısından açılır. Yenilik, çevrim içi içerik arşivi değil; seçim-sonuç ilişkisini deneyimleten ve öğrencinin kendi öğrenmesini görmesini sağlayan senaryo akışıdır.',
             'Çözümümüz öğrencinin karar vermesini, sonucunu görmesini ve yeni bilgiyle tekrar denemesini nasıl sağlıyor?'),
            ('4 · Her ölçümü öğrenci üretimi öğrenme kanıtına çevir', 'Gençlik ve OB8', 0,
             'İklim eğitimi bir poster etkinliğinde bitmemeli. Öğrenci problemi araştırmalı, veriyi yorumlamalı, farklı çözüm seçeneklerini tartmalı, ortak karar vermeli, uygulamayı izlemeli ve sonucu eleştirel biçimde değerlendirmeli. Bu akış OB8 Sürdürülebilirlik Okuryazarlığını bilgi, beceri, tutum ve eylem olarak görünür kılar. Fen dersi su ayak izini hesaplar; matematik veriyi grafikleştirir; Türk dili ve edebiyatı 60 saniyelik hikâyeyi kurar; bilişim prototipi geliştirir.',
             'Bir öğrencinin proje sonunda artık sadece bildiğini değil, yapabildiğini ve savunabildiğini hangi ürünle göstereceğiz?'),
            ('5 · İçeriği erişilebilir ve farklı cihazlarda kullanılabilir tasarla', 'Erişim ve kapsayıcılık', 0,
             'Görevler telefonda hızlı açılmalı; klavyeyle, ekran okuyucuyla ve düşük bağlantı hızında kullanılabilmeli. Metin sade, seçim alanları büyük, geri bildirim açık olmalı. QR basılı materyali zorunlu kılmaz: kısa bağlantı aynı zamanda paylaşılabilmeli ve sitede menüden erişilebilmelidir.',
             'Telefonu, klavyesi veya QR okuyucusu olmayan bir öğrenci aynı göreve nasıl ulaşabilir?'),
            ('6 · Mevcut siteyle 30 günlük dijital pilot uygula', 'İlk uygulanabilirlik · 10 puan', 10,
             'Yeni donanım veya okul mekânı gerekmez. İlk hafta öğrenciler senaryo kaynaklarını inceler; ikinci hafta ekipler yeni görev yazar; üçüncü hafta görevler siteye eklenir ve telefonlarda denenir; dördüncü hafta öğrenciler anlaşılabilirlik ve öğrenme geri bildirimiyle içerikleri iyileştirir. QR kodlar hazır olana kadar menüdeki Dijital Görevler bağlantısı pilotu başlatır.',
             'İlk görevi bu hafta sitede yayımlamak için hangi içerik, sorumlu ve kontrol adımları gerekiyor?'),
            ('7 · Gerçek çevresel sonuç ile öğrenme etkisini ayrı raporla', 'İklimsel ve sosyal katkı · 20 puan', 20,
             'Platform doğrudan kilogram atık veya karbon tasarrufu üretmiş gibi sunulamaz. Gerçek dijital göstergeleri kullanın: görev tamamlama, senaryo cevap başarısı, içerik erişilebilirliği ve öğrenci geri bildirimi. Bu göstergeler öğrenme/katılım etkisini anlatır; fiziksel kaynak tasarrufu kanıtı değildir. Öğrenci ön-test/son-test tasarlarsa ölçüm yöntemini, kapsamını ve sınırlılığını açıkça belirtin.',
             'Hangi sonuç gerçekten ölçüldü; hangisi yalnızca ileride beklenen çevresel katkı?'),
            ('8 · Beş slaytı jüri cetveline ve gerçek kanıta bağla', 'Başvuru hazırlığı', 0,
             'Sunumu son gece yazmayın. Slayt 1 problemi veri ve OB8 perspektifiyle kurar; slayt 2 çözümün çalışma prensibini ve farkını gösterir; slayt 3 pilot yol haritasını, bütçeyi, MEB stratejisi bağlantısını ve riskleri açıklar; slayt 4 çevresel ve sosyal göstergeleri verir; slayt 5 sürdürülebilirlik ve yaygınlaştırmayı kanıtlar. Her slayt tek bir iddia taşısın ve iddia bir veri, görsel veya pilot çıktısıyla desteklensin.',
             'Jüri sunumdan sonra yalnızca bir slaytı hatırlayacaksa, o slayt projenizin hangi vazgeçilmez kanıtını taşımalı?'),
            ('9 · Öğrencinin kendi sesiyle dijital proje günlüğü oluştur', 'Öğrenci sahiplenmesi · 15 puan', 15,
             'Öğrenciler fikir araştırması, senaryo yazımı, kaynak doğrulaması, site testi ve yapılan değişikliği kendi cümleleriyle anlatır. Kısa video şartnameye uygunsa en fazla bir dakika tutulur; çekim yapmak istemeyen öğrenciler yazılı/sesli alternatifle katkı sunabilir. Öğrenci katkısını görünür kılmak için ekipteki görev dağılımını ve sürüm notlarını saklayın.',
             'Takımdaki her öğrenci Ben bu projede neyi değiştirdim? sorusuna kendi kelimeleriyle nasıl cevap verecek?'),
            ('10 · Başka okulların da çoğaltabileceği dijital görev seti yayınla', 'Sürdürülebilirlik ve etik', 0,
             'Senaryo yazım şablonunu, kaynak gösterme biçimini, görev ölçütlerini ve erişilebilirlik kontrol listesini site üzerinde paylaşın. Kişisel veri toplamadan öğrencilerin kendi tarayıcılarında sonuçlarını görebilmelerini sağlayın. Üçüncü taraf içeriklerin lisansını belirtin; çevresel etkiyi kanıtsız iddia etmeyin. Başka bir okul yalnızca internet erişimiyle görevleri kullanabilsin ve yeni senaryo katkısı yapabilsin.',
             'Bu çözüm başka bir okula taşındığında hangi parçaları değişmeden kalmalı, hangi parçaları yerel koşula göre uyarlanmalı?'),
        ]
        for order, (title, eyebrow, score, body, prompt) in enumerate(sections, start=1):
            GuideSection.objects.update_or_create(
                guide=guide,
                order=order,
                defaults={
                    'title': title,
                    'eyebrow': eyebrow,
                    'score_weight': score,
                    'body': body,
                    'prompt': prompt,
                    'is_published': True,
                },
            )
        self.stdout.write(self.style.SUCCESS(f'COP31 rehberi hazır: {guide.sections.count()} bölüm.'))
