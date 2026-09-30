from django.core.management.base import BaseCommand

from core.models import GuideSection, IdeathonGuide


class Command(BaseCommand):
    help = 'Create or update the COP31 ideathon guide content.'

    def handle(self, *args, **options):
        guide, _ = IdeathonGuide.objects.update_or_create(
            pk=1,
            defaults={
                'title': 'Tabaktan iklime: okul gıda sistemini yeniden tasarla',
                'subtitle': 'Öğrencinin topladığı kanıttan, ölçülebilir ve tekrarlanabilir 30 günlük okul pilotuna',
                'introduction': "Özgün proje, yeni bir slogan veya uygulama ekranı değil; okulun gerçek kararını değiştiren ve etkisini tartımla gösterebilen bir sistemdir. Bu dosya, ön eleme cetvelindeki beş ölçüte göre iş üretmek için tasarlandı. En ayırt edici fikir: öğrencilerin ertesi günün porsiyon talebini tahmin ettiği, mutfağın yalnızca toplu gerçekleşen sayıyı paylaştığı ve haftalık tahmin hatasının birlikte öğrenmeye dönüştüğü “Yarın Kaç Porsiyon?” döngüsü. Kimseyi ya da tabağını puanlamaz; sistemi iyileştirir.",
                'source_url': 'https://meslegimhayatim.meb.gov.tr/cop31/Yarisma_Sartnamesi_ve_Basvuru_Rehberi.pdf',
                'is_published': True,
            },
        )
        sections = [
            ('1 · Okulun gıda kaybı parmak izini çıkar', 'Problem ve kanıt · 30 puan', 30,
             'Beş okul günü boyunca yalnızca toplu ve yenilebilir yemek artığını tartın; menü, gün ve porsiyon sayısını kaydedin. Aynı hafta anonim kısa anketle öğrencilerin porsiyon seçimi nedenlerini sorun ve resmî kaynakla iklim-gıda bağını doğrulayın. Kişileri veya tabakları fotoğraflamayın. Jüriye tarihli ham ölçüm, yöntem ve başlangıç değerini gösterin; henüz toplanmamış veriyi sonuç gibi sunmayın.',
             'Bir haftada hangi sayıyı ölçersek bu problem artık yalnızca bir kanaat değil, savunulabilir bir kanıt olur?'),
            ('2 · Bir öğünün su-gıda-iklim pasaportunu çiz', 'Gıda sistemi', 0,
             'Öğrenciler bir okul öğününü kaynağından artığa kadar haritalar: üretim, su, saklama, taşıma, porsiyon ve atık. Her durağa gözlenebilir bir iklim riski ile gıda güvenliği önlemi ekleyin. Bu özgün görsel, çözümün tek başına çöp kutusuna odaklanmadığını ve nerede müdahale edeceğini açıkça gösterir.',
             'Çözümünüz gıdanın hangi durağında en büyük kaybı azaltıyor ve neden tam orası?'),
            ('3 · “Yarın Kaç Porsiyon?” tahmin döngüsünü prototiple', 'Özgün çözüm · 25 puan', 25,
             'Öğrenci ekipleri haftanın günü, menü tercihi ve geçen haftanın anonim toplam porsiyon tüketimine bakarak yarının talebini tahmin eder. Mutfak yalnızca üretilen ve kalan toplam porsiyonu paylaşır; öğrenci isimleri, sağlık bilgisi ve bireysel tabak kaydı tutulmaz. Haftalık tahmin-gerçekleşme farkı görünür olur ve menü/porsiyon kararı okul ekibiyle iyileştirilir. Özgünlük, tahmin + gerçek geri bildirim + ortak karar döngüsüdür; pahalı sensör gerektirmez.',
             'Mevcut uygulamalardan hangi davranış döngüsünü farklı kuruyoruz: fark et, seç, uygula, ölç ve yeniden tasarla?'),
            ('4 · Her ölçümü öğrenci üretimi öğrenme kanıtına çevir', 'İklimsel ve sosyal katkı · 20 puan', 20,
             'İklim eğitimi bir poster etkinliğinde bitmemeli. Öğrenci problemi araştırmalı, veriyi yorumlamalı, farklı çözüm seçeneklerini tartmalı, ortak karar vermeli, uygulamayı izlemeli ve sonucu eleştirel biçimde değerlendirmeli. Bu akış OB8 Sürdürülebilirlik Okuryazarlığını bilgi, beceri, tutum ve eylem olarak görünür kılar. Fen dersi su ayak izini hesaplar; matematik veriyi grafikleştirir; Türk dili ve edebiyatı 60 saniyelik hikâyeyi kurar; bilişim prototipi geliştirir.',
             'Bir öğrencinin proje sonunda artık sadece bildiğini değil, yapabildiğini ve savunabildiğini hangi ürünle göstereceğiz?'),
            ('5 · Gıda güvenliğini azaltım hedefiyle birlikte koru', 'Gıda güvenliği', 0,
             'Gıda güvenliğini su kaynaklarından ayrı düşünmeyin. Menü planlama, porsiyon talebi tahmini, doğru saklama ve kuraklığa uyumlu su kullanımını tek bir pilotta izleyin. Gıda artığını tartmak, onu yeniden sunmayı veya paylaşmayı önermek anlamına gelmez: böyle bir karar ancak okulun gıda güvenliği sorumlusu ve yürürlükteki kurallar doğrultusunda alınabilir. Hangi davranışın ne kadar suyu ve gıdayı koruduğunu ölçün; güvenliği azaltım hedefinin önüne koyun.',
             'Pilotun ilk ayında bir öğrencinin veya okul çalışanının günlük kararını değiştirecek en küçük ama en güçlü müdahale nedir?'),
            ('6 · 30 günlük düşük maliyetli pilotu başlat', 'İlk uygulanabilirlik · 10 puan', 10,
             'İlk uygulanabilirlik puanı için büyük bütçeli bir gelecek vaadi değil, güvenli ve tekrarlanabilir bir başlangıç önerin. 1. hafta ölç, 2. hafta küçük müdahaleyi dene, 3. hafta sonuçları karşılaştır, 4. hafta sistemi iyileştir. Rolleri açıkça bölün: öğrenci veri ekibi, mutfak veya tesis ekibi, öğretmen rehber, iletişim ekibi. İhtiyaç listesini, tahmini maliyeti, izinleri ve risk azaltma planını yazın.',
             'Pilot için yarın okulda hangi üç kişi, hangi malzemeyle, kaç dakikada ilk ölçümü yapabilir?'),
            ('7 · İklim etkisini tahminden ölçüme ayır', 'Ölçülebilir etki', 15,
             'İyi niyet ölçülebilir etki değildir. Başlangıç değeri, hedef, ölçüm sıklığı ve sorumlu kişisi olan göstergeler seçin. Örnekler: öğün başına gram gıda artığı, haftalık çöpe giden porsiyon sayısı, litre su tüketimi, katılan öğrenci sayısı, sürdürülebilirlik bilgi testi puanı, tekrar eden davranış oranı ve pilotu başka sınıfa taşıyan ekip sayısı. Çevresel ve sosyal göstergeleri birlikte izleyin; çünkü daha az atık kadar daha güçlü bir öğrenme ve adil katılım da sonuçtur.',
             'Başlangıç değerimiz nedir, 30 gün sonunda hangi değişikliği görürsek pilotu büyütmeye karar vereceğiz?'),
            ('8 · Beş slaytı jüri cetveline ve gerçek kanıta bağla', 'Başvuru hazırlığı', 0,
             'Sunumu son gece yazmayın. Slayt 1 problemi veri ve OB8 perspektifiyle kurar; slayt 2 çözümün çalışma prensibini ve farkını gösterir; slayt 3 pilot yol haritasını, bütçeyi, MEB stratejisi bağlantısını ve riskleri açıklar; slayt 4 çevresel ve sosyal göstergeleri verir; slayt 5 sürdürülebilirlik ve yaygınlaştırmayı kanıtlar. Her slayt tek bir iddia taşısın ve iddia bir veri, görsel veya pilot çıktısıyla desteklensin.',
             'Jüri sunumdan sonra yalnızca bir slaytı hatırlayacaksa, o slayt projenizin hangi vazgeçilmez kanıtını taşımalı?'),
            ('9 · Öğrencinin kendi sesiyle 60 saniyelik saha günlüğü çek', 'Öğrenci sahiplenmesi · 15 puan', 15,
             'Video profesyonel görünmekten önce gerçek görünmelidir. Her öğrenci aynı metni okumak yerine kendi rolünü ve projeyle neden ilgilendiğini bir cümleyle anlatsın. Bir öğrenci problemi, biri çözüm prototipini, biri veriyi, biri de okulda yaratılacak değişimi üstlensin. Görsel olarak okulun gerçek mekânlarını kullanın; ses anlaşılır, bağlantı erişilebilir ve süre bir dakika olsun. Bu, projenin yetişkinler tarafından yazılmış bir fikir değil, öğrencilerin sahiplendiği bir çözüm olduğunu gösterir.',
             'Takımdaki her öğrenci Ben bu projede neyi değiştirdim? sorusuna kendi kelimeleriyle nasıl cevap verecek?'),
            ('10 · Açık kaynaklı okul kitiyle çoğalt, güvenle geliştir', 'Etik ve yaygınlaştırma', 0,
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
