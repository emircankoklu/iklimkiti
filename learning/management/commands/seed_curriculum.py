from django.core.management.base import BaseCommand
from django.utils.text import slugify

from learning.models import InformationCard, LessonModule, MindMap, MindMapNode, QuestionAnswer, Topic


class Command(BaseCommand):
    help = 'Create the Turkish food, climate, and education curriculum.'

    def handle(self, *args, **options):
        topics = [
            {
                'title': 'Gıda güvenliği ve iklim krizi',
                'theme': 'Gıda güvenliği · 30 puanlık problem kanıtı',
                'description': 'İklim değişikliği; üretim, su, toprak, depolama ve sofraya erişim zincirinin her halkasını etkiler. Bu konu, güvenli ve yeterli gıdaya erişimi okul yaşamından başlayarak kanıtlamayı öğretir.',
                'key_question': 'İklim değişikliği güvenli ve yeterli gıdaya erişimimizi nasıl etkiliyor?',
                'action_text': 'Okulunuzda gıdanın nerede risk aldığını ölçün, görünür kılın ve küçük bir pilotla azaltın.',
                'modules': [
                    ('Gıdanın tarladan tabağa yolculuğu', 'Su, toprak, enerji, taşıma, soğuk zincir ve atık halkalarını tek bir gıda ürünü üzerinden izleyin.', 'Güvenli gıdaya erişim yalnızca üretim miktarı değil; saklama, hijyen, adil paylaşım ve iklim dayanıklılığı meselesidir.'),
                    ('İklim riski ve gıda riski haritası', 'Kuraklık, sıcak hava, sel ve enerji kesintisinin okul mutfağına etkisini risk matrisiyle inceleyin.', 'Okulunuzda hangi risk hem en olası hem de en ağır sonucu doğuruyor?'),
                    ('Okul için güvenli gıda protokolü', 'Menü planlama, porsiyon, saklama ve israf ölçümünü bir araya getiren uygulanabilir bir okul protokolü tasarlayın.', 'Protokolünüz kimin hangi kararı ne zaman alacağını açıkça göstermeli.'),
                ],
                'qas': [
                    ('Problem gerçekten var mı, nasıl kanıtlarız?', 'Bir haftalık gözlem, üç günlük gıda artığı ölçümü, anonim öğrenci anketi ve resmî kaynak karşılaştırması yaparak başlangıç değerini kurarız. Böylece sorun yalnızca küresel bir tehdit değil, okulda ölçülebilen bir gıda güvenliği açığı olur.', 'Problem ve kanıt'),
                    ('Çözümümüz gıda güvenliğini nasıl artırıyor?', 'Çözüm; menü, porsiyon ve saklama kararlarını gerçek okul verisiyle iyileştirir. Daha az atık, daha doğru planlama ve daha güvenli saklama aynı anda kaynak verimliliği ve gıdaya erişim sağlar.', 'İklimsel ve sosyal katkı'),
                    ('İlk pilot nerede ve nasıl başlayacak?', 'Bir sınıf ve bir öğünle 30 günlük pilot başlatılır. Öğrenci veri ekibi artığı tartar, mutfak ekibi menü ve porsiyonu izler, öğretmen haftalık değerlendirmeyi yürütür.', 'İlk uygulanabilirlik'),
                ],
                'cards': [('Kanıt', 'Gıda güvenliği, gıdanın varlığı kadar güvenli, erişilebilir ve sürdürülebilir olmasıdır.'), ('Veri', 'Başlangıç ölçümü olmadan proje etkisi iddia değil, tahmindir.'), ('Eylem', 'Bir öğünü ölçmek, bütün okul sistemi hakkında düşünmenin küçük ama güçlü başlangıcıdır.')],
                'nodes': ['İklim riskleri', 'Su ve toprak', 'Üretim', 'Depolama ve hijyen', 'Okul mutfağı', 'Ölçüm ve pilot'],
            },
            {
                'title': 'Gıda kaybı, israf ve sıfır atık',
                'theme': 'Sıfır atık · 25 puanlık yenilik',
                'description': 'Gıda kaybını yalnızca çöp kutusundaki son adım olarak değil; planlama, satın alma, porsiyon, tüketim ve paylaşım kararlarının toplamı olarak ele alın.',
                'key_question': 'Okulda yenilebilir gıda neden atığa dönüşüyor ve döngüyü nerede kırabiliriz?',
                'action_text': 'Atığın kaynağını bulup öğrencinin davranışını değiştiren döngüsel bir sistem tasarlayın.',
                'modules': [
                    ('Atığın kaynağını bul', 'Atığı türüne, zamanına ve nedenine göre sınıflandırın; yalnızca miktarı değil, sebebi de kaydedin.', 'Tabağa alınan ama yenmeyen gıda ile yanlış saklama nedeniyle bozulan gıda aynı çözümü gerektirmez.'),
                    ('Döngüsel okul mutfağı', 'Ölçüm, yeniden planlama, güvenli paylaşım ve kompost farkındalığını tek bir döngüde tasarlayın.', 'Atığın oluşmasını önlemek, oluştuktan sonra yönetmekten daha yüksek etki yaratır.'),
                    ('Davranış değişikliği laboratuvarı', 'Mesaj, görünür veri, sınıf hedefi ve geri bildirim döngülerini test ederek hangi müdahalenin işe yaradığını karşılaştırın.', 'En yaratıcı fikir, öğrenciyi suçlamadan seçimini değiştiren fikirdir.'),
                ],
                'qas': [
                    ('Çözümümüz mevcut kampanyalardan neden farklı?', 'Poster asmak yerine davranış döngüsü kuruyoruz: öğrenci artığı görür, nedenini seçer, sınıf veriyi takip eder, mutfak planı güncellenir ve sonuç yeniden paylaşılır. Sistem, tek seferlik kampanyayı sürekli öğrenmeye çevirir.', 'Çözümün yenilikçi potansiyeli'),
                    ('Metan ve karbon etkisini nasıl açıklayacağız?', 'Önlenen gıda atığı; üretim, taşıma, soğutma ve bertaraf için harcanan kaynakların da boşa gitmesini önler. Pilotumuz kilogram atığı ve öğün başına düşen artığı izleyerek emisyon azaltımına ilişkin şeffaf bir gösterge üretir.', 'Ölçülebilir çevresel etki'),
                    ('Öğrenci sahiplenmesi nasıl görünecek?', 'Her öğrenci kendi sınıfındaki ölçüm, iletişim, tasarım veya sunum rolünü üstlenir. Video ve sunumda herkes “hangi veriyi topladım, hangi kararı değiştirdim?” sorusunu kendi diliyle cevaplar.', 'Öğrenci sahiplenmesi'),
                ],
                'cards': [('Gerçek', 'İsrafın nedenini bilmeden yalnızca miktarı azaltmaya çalışmak sistemi körleştirir.'), ('Mit', 'Sıfır atık yalnızca geri dönüşüm kutusu değildir; satın almadan tüketime kadar önleme tasarımıdır.'), ('Eylem', 'Bir haftalık atık günlüğü, çözümün en değerli ilk prototipidir.')],
                'nodes': ['Planlama', 'Porsiyon', 'Tüketim', 'Paylaşım', 'Kompost ve döngü', 'Geri bildirim'],
            },
            {
                'title': 'Su kaynakları, kuraklık ve akıllı kullanım',
                'theme': 'Gıda güvenliği · kaynak verimliliği',
                'description': 'Su kaynaklarını yalnızca musluktan akan su olarak değil, her gıdanın üretiminde kullanılan görünmez kaynak olarak okuyun. Kuraklığa uyum, ölçüm ve adil kullanım üzerinden tasarlanır.',
                'key_question': 'Daha az suyla daha güvenli gıda ve daha dirençli okul nasıl mümkün olur?',
                'action_text': 'Su tüketimini görünür bir göstergeye çevirin ve gıda kararlarıyla birlikte yönetin.',
                'modules': [
                    ('Su ayak izini oku', 'Bir öğünün su ayak izini üretimden yıkamaya kadar basit bir sistem haritasıyla inceleyin.', 'Görünmez suyu görünür kılmak, tüketim kararının sonuçlarını anlamayı sağlar.'),
                    ('Kuraklığa dayanıklı okul', 'Sızıntı kontrolü, verimli sulama, yağmur suyu farkındalığı ve bitki seçimini okul planına bağlayın.', 'Her teknik çözümün bakım sorumlusu ve ölçüm yöntemi bulunmalı.'),
                    ('Su verisiyle karar ver', 'Sayaç, gözlem ve anket verilerini haftalık göstergeye çevirip hangi müdahalenin etkili olduğunu test edin.', 'Veri, korkutmak için değil daha adil ve akıllı karar almak için kullanılır.'),
                ],
                'qas': [
                    ('Su ve gıda güvenliği neden birlikte düşünülmeli?', 'Tarımın verimi, gıdanın fiyatı ve okulun beslenme güvenliği suya bağlıdır. Su verimliliği sağlayan çözüm aynı zamanda kuraklık riskine, üretim kesintilerine ve kaynak eşitsizliğine karşı dayanıklılık üretir.', 'Problem ve kanıt'),
                    ('Çevresel etkiyi hangi göstergelerle ölçeceğiz?', 'Haftalık litre tüketimi, sızıntı sayısı, verimli sulanan alan ve öğrencilerin su bilgisi ön-test/son-test puanı birlikte izlenir. Böylece fiziksel tasarruf ile eğitim etkisi aynı tabloda görülür.', 'Ölçülebilir çevresel ve sosyal etki'),
                    ('Düşük bütçeli çözüm ne olabilir?', 'İlk pilot pahalı sensörle değil, sayaç okuma, sızıntı gözlemi, sınıf su günlüğü ve doğru sulama saatlerinin takibiyle başlar. Etki kanıtlanırsa teknik yatırım için güçlü bir gerekçe oluşur.', 'İlk uygulanabilirlik'),
                ],
                'cards': [('Bilgi', 'Su ayak izi, bir ürünün tüm yaşam döngüsünde kullandığı doğrudan ve dolaylı suyu düşünmeyi sağlar.'), ('Soru', 'Bir litre suyu kurtarmanın okul topluluğunda hangi davranış karşılığı var?'), ('Eylem', 'Sızıntıyı bildirmek teknik olduğu kadar yurttaşlık sorumluluğudur.')],
                'nodes': ['Su döngüsü', 'Tarım ve gıda', 'Kuraklık', 'Okul altyapısı', 'Verimli kullanım', 'Adil paylaşım'],
            },
            {
                'title': 'Sürdürülebilir tarım, toprak ve biyoçeşitlilik',
                'theme': 'Sürdürülebilir tarım · ekolojik erdem',
                'description': 'Toprağı yalnızca üretim yüzeyi değil, karbon tutan, suyu filtreleyen ve canlılığı taşıyan ortak bir ekosistem olarak keşfedin.',
                'key_question': 'Toprağı koruyan tarım hem gıda güvenliğini hem iklim direncini nasıl güçlendirir?',
                'action_text': 'Okul bahçesi, yerel üretici ve mevsimsel beslenme üzerinden küçük bir yaşayan laboratuvar kurun.',
                'modules': [
                    ('Toprağın canlı hikâyesi', 'Organik madde, su tutma, mikroorganizmalar ve biyoçeşitlilik arasındaki ilişkiyi gözlemleyin.', 'Sağlıklı toprak, iklim stresinde üretimin sigortasıdır.'),
                    ('Mevsimsel ve yerel gıda', 'Bir ürünün mevsim, taşıma, saklama ve beslenme değerini birlikte değerlendirin.', 'Yerel tercihi romantik bir slogan değil, veri ve erişilebilirlik meselesi olarak ele alın.'),
                    ('Okul bahçesi pilotu', 'Kompost, yerel tohum, yağmur suyu ve öğrenci gözlem defterini bir araya getiren küçük bir uygulama planlayın.', 'Pilot, bakım ve devamlılık sorumluluğu paylaşılmadığında yaşayamaz.'),
                ],
                'qas': [
                    ('Yenilik nerede?', 'Yenilik tek bir bahçe kurmakta değil; öğrencinin toprağı gözlemlediği, mutfak atığının kaynağa dönüştüğü ve gıda kararlarının veriye dayandığı kapalı öğrenme döngüsündedir.', 'Çözümün yenilikçi potansiyeli'),
                    ('OB8 hangi kazanımları görünür kılıyor?', 'Öğrenci canlı sistemleri gözlemler, kanıt toplar, kaynaklar arasındaki ilişkiyi açıklar, ortak bakım sorumluluğu alır ve uygulamasının sonucunu değerlendirir. Bilgi eyleme, eylem değere dönüşür.', 'Maarif Modeli ve OB8'),
                    ('Nasıl yaygınlaştıracağız?', 'Bahçe tasarımını tek tip kopyalamak yerine ölçüm formları, düşük maliyetli malzeme listesi ve bakım rol kartlarıyla paketleriz. Her okul kendi iklimine ve alanına göre uyarlayabilir.', 'Sürdürülebilirlik ve yaygınlaştırma'),
                ],
                'cards': [('Gerçek', 'Biyoçeşitlilik, tarımın iklim şoklarına karşı seçeneklerini ve dayanıklılığını artırır.'), ('Uyarı', 'Toprağı yalnızca verimle değerlendirmek, ekosistem hizmetlerini görünmez kılar.'), ('Eylem', 'Bir avuç toprağı gözlemlemek, iklim sistemini anlamaya açılan somut bir kapıdır.')],
                'nodes': ['Toprak canlılığı', 'Su tutma', 'Biyoçeşitlilik', 'Yerel üretim', 'Kompost', 'Okul bahçesi'],
            },
            {
                'title': 'İklim okuryazarlığı ve öğrenci eylemi',
                'theme': 'Gençlik ve eğitim · 20 puan OB8',
                'description': 'İklim bilgisini ezberden çıkarıp araştırma, eleştirel düşünme, iş birliği, iletişim ve eylem becerisine dönüştüren öğrenme tasarımını keşfedin.',
                'key_question': 'Öğrenci iklim bilgisini gerçek bir okul değişimine nasıl dönüştürebilir?',
                'action_text': 'Öğrenciye hazır cevap vermek yerine kanıt toplama, çözüm üretme ve sonucu savunma görevi verin.',
                'modules': [
                    ('İklim iddiasını test et', 'Bir iddianın veri, kaynak, kapsam ve belirsizlik açısından nasıl değerlendirileceğini öğrenin.', 'İklim okuryazarı öğrenci duyduğu her bilgiyi paylaşmaz; önce sorar ve doğrular.'),
                    ('Disiplinler arası çözüm atölyesi', 'Fen, matematik, bilişim, dil ve görsel iletişimi aynı proje çıktısında buluşturun.', 'Gerçek problemler ders çizelgesindeki sınırları aşar; iyi ekip farklı güçlü yanları birleştirir.'),
                    ('Öğrenci anlatısı ve 60 saniye', 'Projenin nedenini, rolünü ve etkisini doğal dille anlatan takım videosu ve sunum provası hazırlayın.', 'Sahiplenme, metni ezberlemek değil kararı neden verdiğini açıklayabilmektir.'),
                ],
                'qas': [
                    ('Öğrenci sahiplenmesi nasıl kanıtlanır?', 'Öğrenciler veri toplama, prototip, iletişim ve sunum rollerini kendileri üstlenir. Her biri kendi kararını ve öğrendiği dersi açıklayabildiğinde proje yetişkin metni olmaktan çıkar.', 'Öğrenci sahiplenmesi'),
                    ('Eğitim etkisini nasıl ölçeceğiz?', 'Kısa ön-test/son-test, öğrenci yansıtma günlüğü, katılım sayısı ve gerçek davranış göstergesi birlikte kullanılır. Amaç yalnızca ne bildiklerini değil, neyi uyguladıklarını görmektir.', 'Ölçülebilir sosyal etki'),
                    ('Eşit katılım nasıl sağlanır?', 'Konuşma, veri, tasarım, saha ve sunum gibi farklı roller tanımlanır; özel gereksinimleri olan öğrenciler için erişilebilir materyal ve alternatif katılım yolları baştan planlanır.', 'Etik ve erişilebilirlik'),
                ],
                'cards': [('Bilgi', 'İklim okuryazarlığı veri okumayı, belirsizliği yönetmeyi ve eylem seçimini birlikte içerir.'), ('Soru', 'Bir öğrenci bu hafta hangi küçük kararı değiştirirse öğrenme gerçek hayata taşınmış olur?'), ('Eylem', 'Her ekip toplantısı sonunda bir sonraki ölçülebilir adımı yazın.')],
                'nodes': ['Kanıt okuma', 'Eleştirel düşünme', 'İş birliği', 'Yeşil beceriler', 'İletişim', 'Eylem ve yansıtma'],
            },
            {
                'title': 'Okul iklim çözümü tasarım stüdyosu',
                'theme': 'Uygulanabilirlik · 10 puan pilot',
                'description': 'Bu konu, seçtiğiniz gıda veya eğitim problemini 30 günlük bir okul pilotuna, beş slaytlık sunuma ve ölçülebilir yaygınlaştırma planına dönüştürür.',
                'key_question': 'Fikrimizi güvenli, düşük maliyetli ve ölçülebilir bir okul pilotuna nasıl çeviririz?',
                'action_text': 'Problem, çözüm, pilot, gösterge ve yaygınlaştırma cümlelerinizi tek bir proje kanvasında birleştirin.',
                'modules': [
                    ('Problem-çözüm kanvası', 'Hedef kitleyi, kök nedeni, mevcut alternatifi, çözüm mekanizmasını ve varsayımları tek sayfada netleştirin.', 'İyi kanvas fikir kalabalığını azaltır ve jürinin cevabı hızlı görmesini sağlar.'),
                    ('Risk, bütçe ve yol haritası', '30 günlük takvim, görev paylaşımı, izinler, tahmini bütçe, veri güvenliği ve başarısızlık senaryosunu yazın.', 'Uygulanabilirlik büyük söz değil, küçük adımların sıralı ve sorumlusu belli olmasıdır.'),
                    ('Beş slayt ve jüri provası', 'Beş slaytı beş iddiaya indirin; beş dakikalık anlatım ve beş dakikalık soru-cevap provası yapın.', 'Her cevabın bir veri, bir örnek ve bir sonraki adımı olmalı.'),
                ],
                'qas': [
                    ('Jüriye en kısa güçlü cevabımız nedir?', 'Okulumuzda ölçtüğümüz şu problem, şu davranış döngüsünden kaynaklanıyor; önerdiğimiz çözüm şu mekanizmayla 30 günde şu göstergeyi değiştirecek ve sonuç iyi olursa şu okullara yayılacak.', 'Canlı sunum ve takım dinamizmi'),
                    ('Risk gerçekleşirse ne yapacağız?', 'Her kritik varsayım için erken uyarı göstergesi ve alternatif plan yazılır. Pilot düşük etki üretirse fikri savunmak yerine veriyi okuyup müdahaleyi değiştiririz; bu da öğrenme çıktısıdır.', 'Teknik uygulanabilirlik'),
                    ('Tam puana giden dosya nasıl kontrol edilir?', 'Bir sayfalık çözüm formu, beş slaytlık PDF, erişilebilir bir dakikalık video, kaynakça, veri/izin planı ve pilot takvimi birlikte kontrol edilir. Hiçbir iddia kaynaksız veya ölçümsüz bırakılmaz.', 'Başvuru hazırlığı'),
                ],
                'cards': [('Kontrol', 'Her çözüm iddiasının yanında kanıtı, sahibi, süresi ve ölçüm yöntemi bulunmalıdır.'), ('Uyarı', 'Bütçesi, izni ve sorumlusu olmayan prototip yalnızca iyi niyettir.'), ('Eylem', 'Bugün bir sayfalık kanvası doldurun; yarın ilk ölçümü başlatın.')],
                'nodes': ['Problem kanıtı', 'Özgün çözüm', 'Pilot planı', 'Etki göstergeleri', 'Sunum', 'Yaygınlaştırma'],
            },
        ]
        for order, data in enumerate(topics, start=1):
            topic, _ = Topic.objects.update_or_create(
                slug=slugify(data['title']),
                defaults={
                    'title': data['title'],
                    'theme': data['theme'],
                    'description': data['description'],
                    'key_question': data['key_question'],
                    'action_text': data['action_text'],
                    'target_age': 'Lise öğrencileri',
                    'estimated_duration_minutes': 45,
                    'order': order,
                    'is_published': True,
                },
            )
            for module_order, (title, description, challenge) in enumerate(data['modules'], start=1):
                LessonModule.objects.update_or_create(
                    topic=topic,
                    slug=slugify(title),
                    defaults={
                        'title': title,
                        'description': description,
                        'problem_statement': data['key_question'],
                        'real_life_example': challenge,
                        'action_challenge': 'Ekibinizle kanıtı, sorumluyu ve ilk ölçüm tarihini yazın.',
                        'order': module_order,
                        'is_published': True,
                    },
                )
            for card_order, (title, content) in enumerate(data['cards'], start=1):
                InformationCard.objects.update_or_create(
                    topic=topic,
                    title=title,
                    defaults={'content': content, 'card_type': 'question' if title == 'Soru' else 'fact', 'is_published': True},
                )
            for qa_order, (question, answer, dimension) in enumerate(data['qas'], start=1):
                QuestionAnswer.objects.update_or_create(
                    topic=topic,
                    question=question,
                    defaults={'answer': answer, 'score_dimension': dimension, 'order': qa_order, 'is_published': True},
                )
            mind_map, _ = MindMap.objects.update_or_create(
                topic=topic,
                slug=slugify(f'{data["title"]} zihin haritası'),
                defaults={'title': f'{data["title"]}: zihin haritası', 'description': 'Problemden ölçülebilir eyleme uzanan bağlantılar.', 'is_published': True},
            )
            for node_order, node_title in enumerate(data['nodes'], start=1):
                MindMapNode.objects.update_or_create(
                    mind_map=mind_map,
                    title=node_title,
                    defaults={'description': f'{node_title} için kanıt, karar ve eylem bağlantısını kurun.', 'position_x': node_order * 120, 'position_y': (node_order % 2) * 120},
                )
        self.stdout.write(self.style.SUCCESS(f'Müfredat hazır: {Topic.objects.filter(is_published=True).count()} konu.'))
