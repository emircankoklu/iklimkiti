from django.core.management.base import BaseCommand

from core.models import GuideSection, IdeathonGuide


class Command(BaseCommand):
    help = 'Create or update the COP31 ideathon guide content.'

    def handle(self, *args, **options):
        guide, _ = IdeathonGuide.objects.update_or_create(
            pk=1,
            defaults={
                'title': 'Gıda ve eğitim için iklim çözümü stüdyosu',
                'subtitle': 'COP31 Maarif İklim İdeathonu için kanıttan prototipe uzanan çalışma alanı',
                'introduction': "Bu stüdyo, İklimKiti'ni yalnızca bilgi veren bir platform olmaktan çıkarıp öğrencilerin gerçek bir okul probleminden ölçülebilir bir iklim çözümü ürettiği yaşayan bir laboratuvara dönüştürür. Her bölüm, ön elemedeki puan cetvelinin bir sorusuna cevap verir: Problem gerçekten var mı, çözüm özgün mü, öğrenciler sahipleniyor mu ve ilk pilot yarın başlayabilir mi?",
                'source_url': 'https://meslegimhayatim.meb.gov.tr/cop31/Yarisma_Sartnamesi_ve_Basvuru_Rehberi.pdf',
                'is_published': True,
            },
        )
        sections = [
            ('Kanıt avı: problemi okulun mutfağında görünür kıl', 'Kanıt ve problem', 30,
             'Gıda güvenliği ve iklim sorununu büyük, soyut cümlelerle değil; okulunuzun bir haftalık yaşamından gelen küçük ama tekrarlanabilir kanıtlarla anlatın. Yemekhanede çöpe giden porsiyonları, kantinde satılmadan kalan ürünleri, su sebilindeki bekleme süresini veya öğrencilerin öğün atlama nedenlerini anonim biçimde gözlemleyin. En az üç veri kaynağı kullanın: gözlem çizelgesi, kısa öğrenci anketi ve güvenilir resmî veya akademik kaynak. Böylece jüriye yalnızca sorun gördüğünüzü değil, sorunu ölçmeyi öğrendiğinizi gösterirsiniz.',
             'Bir haftada hangi sayıyı ölçersek bu problem artık yalnızca bir kanaat değil, savunulabilir bir kanıt olur?'),
            ('Gıdanın görünmeyen yolculuğunu haritala', 'Gıda ve su', 0,
             'Bir elmanın veya okul öğününün tabağa gelene kadar geçtiği yolculuğu çıkarın: tohum, su, toprak, enerji, paketleme, taşıma, soğutma ve atık. Haritanın her durağında iklim riski ile gıda güvenliği riskini yan yana yazın. Kuraklık verimi düşürür; yanlış saklama besin kaybını artırır; plansız üretim ve tüketim israfı büyütür. Bu harita, projenizin yalnızca çöp kutusuna değil, bütün sisteme baktığını kanıtlar.',
             'Çözümünüz gıdanın hangi durağında en büyük kaybı azaltıyor ve neden tam orası?'),
            ('Çözümü ürün değil davranış sistemi olarak tasarla', 'Yenilik ve çözüm', 25,
             'Özgün fikir, yalnızca yeni bir uygulama adı veya sensör eklemek değildir. Öğrencinin kararını değiştiren, öğretmenin işini kolaylaştıran ve okulun mevcut akışına oturan bir sistem kurun. Örneğin öğrenciler yemek artığını fotoğraflayıp puan toplarken mutfak ekibi anonim toplamları görsün; menü planlaması haftalık veriye göre güncellensin; sınıflar çözümün sahibi olsun. Teknoloji, davranış değişikliğini görünür ve sürdürülebilir kıldığı ölçüde değerlidir.',
             'Mevcut uygulamalardan hangi davranış döngüsünü farklı kuruyoruz: fark et, seç, uygula, ölç ve yeniden tasarla?'),
            ('Dersi eyleme, eylemi OB8 becerisine bağla', 'Eğitim ve OB8', 20,
             'İklim eğitimi bir poster etkinliğinde bitmemeli. Öğrenci problemi araştırmalı, veriyi yorumlamalı, farklı çözüm seçeneklerini tartmalı, ortak karar vermeli, uygulamayı izlemeli ve sonucu eleştirel biçimde değerlendirmeli. Bu akış OB8 Sürdürülebilirlik Okuryazarlığını bilgi, beceri, tutum ve eylem olarak görünür kılar. Fen dersi su ayak izini hesaplar; matematik veriyi grafikleştirir; Türk dili ve edebiyatı 60 saniyelik hikâyeyi kurar; bilişim prototipi geliştirir.',
             'Bir öğrencinin proje sonunda artık sadece bildiğini değil, yapabildiğini ve savunabildiğini hangi ürünle göstereceğiz?'),
            ('Su-gıda ikilisini tek bir pilotta buluştur', 'Gıda ve su', 0,
             'Gıda güvenliğini su kaynaklarından ayrı düşünmeyin. Okul mutfağında menü planlaması, porsiyon ölçüsü, doğru saklama, yağmur suyu farkındalığı ve verimli sulama gibi küçük kararları tek bir pilot akışta birleştirin. Çözümünüz hem kuraklığa uyum sağlamalı hem de öğrencinin her gün görebileceği bir sonuç üretmeli. Daha az tüketelim demek yerine, hangi davranışın kaç litre suyu ve kaç kilogram gıda kaybını önlediğini gösterin.',
             'Pilotun ilk ayında bir öğrencinin veya okul çalışanının günlük kararını değiştirecek en küçük ama en güçlü müdahale nedir?'),
            ('Yarın başlayabilecek 30 günlük pilot yaz', 'Uygulanabilirlik', 10,
             'İlk uygulanabilirlik puanı için büyük bütçeli bir gelecek vaadi değil, güvenli ve tekrarlanabilir bir başlangıç önerin. 1. hafta ölç, 2. hafta küçük müdahaleyi dene, 3. hafta sonuçları karşılaştır, 4. hafta sistemi iyileştir. Rolleri açıkça bölün: öğrenci veri ekibi, mutfak veya tesis ekibi, öğretmen rehber, iletişim ekibi. İhtiyaç listesini, tahmini maliyeti, izinleri ve risk azaltma planını yazın.',
             'Pilot için yarın okulda hangi üç kişi, hangi malzemeyle, kaç dakikada ilk ölçümü yapabilir?'),
            ('Etkiyi puan değil gösterge olarak kur', 'Ölçülebilir etki', 15,
             'İyi niyet ölçülebilir etki değildir. Başlangıç değeri, hedef, ölçüm sıklığı ve sorumlu kişisi olan göstergeler seçin. Örnekler: öğün başına gram gıda artığı, haftalık çöpe giden porsiyon sayısı, litre su tüketimi, katılan öğrenci sayısı, sürdürülebilirlik bilgi testi puanı, tekrar eden davranış oranı ve pilotu başka sınıfa taşıyan ekip sayısı. Çevresel ve sosyal göstergeleri birlikte izleyin; çünkü daha az atık kadar daha güçlü bir öğrenme ve adil katılım da sonuçtur.',
             'Başlangıç değerimiz nedir, 30 gün sonunda hangi değişikliği görürsek pilotu büyütmeye karar vereceğiz?'),
            ('Beş slaytlık jüri omurgasını şimdiden prova et', 'Başvuru hazırlığı', 0,
             'Sunumu son gece yazmayın. Slayt 1 problemi veri ve OB8 perspektifiyle kurar; slayt 2 çözümün çalışma prensibini ve farkını gösterir; slayt 3 pilot yol haritasını, bütçeyi, MEB stratejisi bağlantısını ve riskleri açıklar; slayt 4 çevresel ve sosyal göstergeleri verir; slayt 5 sürdürülebilirlik ve yaygınlaştırmayı kanıtlar. Her slayt tek bir iddia taşısın ve iddia bir veri, görsel veya pilot çıktısıyla desteklensin.',
             'Jüri sunumdan sonra yalnızca bir slaytı hatırlayacaksa, o slayt projenizin hangi vazgeçilmez kanıtını taşımalı?'),
            ('Bir dakikada öğrenci sahiplenmesini duyur', 'Başvuru hazırlığı', 15,
             'Video profesyonel görünmekten önce gerçek görünmelidir. Her öğrenci aynı metni okumak yerine kendi rolünü ve projeyle neden ilgilendiğini bir cümleyle anlatsın. Bir öğrenci problemi, biri çözüm prototipini, biri veriyi, biri de okulda yaratılacak değişimi üstlensin. Görsel olarak okulun gerçek mekânlarını kullanın; ses anlaşılır, bağlantı erişilebilir ve süre bir dakika olsun. Bu, projenin yetişkinler tarafından yazılmış bir fikir değil, öğrencilerin sahiplendiği bir çözüm olduğunu gösterir.',
             'Takımdaki her öğrenci Ben bu projede neyi değiştirdim? sorusuna kendi kelimeleriyle nasıl cevap verecek?'),
            ('Risk, etik, erişilebilirlik ve yaygınlaştırma kalkanını kur', 'Etik ve yaygınlaştırma', 0,
             'Gıda ve eğitim projelerinde güven, yenilik kadar önemlidir. Öğrenci fotoğrafı ve anket verisi için açık rıza ve anonimlik planlayın; hassas sağlık veya beslenme bilgisi toplamaktan kaçının; özel gereksinimi olan öğrencilerin katılımını baştan tasarlayın. Üçüncü taraf görsel, veri, müzik ve yazılımın kaynağını belirtin. Pilot işe yaramazsa neyi değiştireceğinizi, işe yararsa başka bir okulun bunu hangi düşük maliyetle uygulayacağını yazın. Sağlam proje, başarısızlığı da öğrenme verisine dönüştürür.',
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
