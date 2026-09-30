from django.core.management.base import BaseCommand

from learning.models import GlossaryTerm, Topic


TERMS = [
    ('Adaptasyon', 'İklim değişikliğinin mevcut ve beklenen etkilerine uyum sağlamak için alınan önlemlerdir. Kuraklığa dayanıklı ürün seçmek, okulun sıcak hava planı hazırlaması veya suyu verimli kullanan sulama sistemine geçmek adaptasyona örnektir. Proje yazarken adaptasyonun hangi riski azalttığını ve kimlerin daha güvenli hâle geldiğini açıkça belirtin.'),
    ('Adil geçiş', 'Düşük karbonlu ve sürdürülebilir bir ekonomiye geçerken hiçbir grubun geride bırakılmamasını ifade eder. Bir okul projesi yalnızca teknik olarak başarılı değil, farklı gelir düzeylerinden ve farklı öğrenme ihtiyaçlarından öğrencilerin katılabileceği kadar erişilebilir olmalıdır.'),
    ('Agroekoloji', 'Tarımı ekolojik ilkelerle birlikte tasarlayan yaklaşımdır. Toprak canlılığını, biyoçeşitliliği, yerel bilgiyi, su verimliliğini ve üreticinin geçimini aynı sistem içinde düşünür. Okul bahçesi veya yerel üretici projesinde tek ürüne değil, ekosistem ilişkilerine bakmayı sağlar.'),
    ('Açık veri', 'Kişisel ve hassas bilgiler korunarak herkesin erişebildiği, yeniden kullanılabilen veridir. İklim ve gıda projesinde resmî istatistikleri, ölçüm yöntemini ve veri tarihini belirtmek iddianın güvenilirliğini artırır.'),
    ('Biyoçeşitlilik', 'Bir ekosistemdeki gen, tür ve yaşam alanı çeşitliliğidir. Biyoçeşitlilik; tozlaşma, zararlıların dengelenmesi, toprağın korunması ve gıda seçeneklerinin devamlılığı için önemlidir. Proje göstergesi olarak gözlenen tür sayısı veya yerel bitki çeşitliliği izlenebilir.'),
    ('Biyolojik mücadele', 'Zararlılarla kimyasal yükü artırmadan doğal düşmanlar ve ekolojik yöntemlerle mücadele etmektir. Sürdürülebilir tarımda toprak ve su sağlığını korur; uygulama planında güvenlik ve uzman danışmanlığı gerekir.'),
    ('Birincil veri', 'Proje ekibinin doğrudan topladığı gözlem, ölçüm, anket veya görüşme verisidir. Okulda bir hafta tartılan gıda artığı birincil veridir. Tarih, yöntem, ölçüm birimi ve sorumluyu kaydetmeden veri kanıt gücünü kaybeder.'),
    ('Bütüncül yaklaşım', 'Bir sorunu yalnızca tek bir sonuç üzerinden değil; çevre, ekonomi, sağlık, eğitim ve adalet ilişkileriyle birlikte değerlendirmektir. Gıda israfını azaltırken beslenme güvenliğini, mutfak iş yükünü ve öğrenci katılımını da hesaba katmak bütüncül yaklaşımdır.'),
    ('Cinsiyet duyarlı iklim eylemi', 'İklim etkilerinin ve kaynaklara erişimin farklı grupları aynı biçimde etkilemediğini dikkate alan planlamadır. Öğrenci verileri toplanırken gönüllülük, mahremiyet ve ayrımcılık karşıtlığı korunmalıdır.'),
    ('Döngüsel ekonomi', 'Ürün ve malzemelerin mümkün olduğunca uzun süre değerini koruduğu, atığın tasarım aşamasında azaltıldığı ekonomik modeldir. Gıda için önleme, güvenli paylaşım, yeniden değerlendirme ve kompost adımlarını; yalnızca geri dönüşümden daha geniş bir çerçevede ele alır.'),
    ('Ekolojik ayak izi', 'Bir kişinin, kurumun veya ürünün kullandığı kaynakları ve oluşturduğu çevresel baskıyı ifade eden göstergedir. Projede ayak izi kullanırken kapsamı, veri kaynağını ve hesap varsayımlarını belirtin; tek bir sayı her şeyi anlatmaz.'),
    ('Ekosistem hizmetleri', 'Doğanın insanlara sağladığı su filtreleme, tozlaşma, karbon tutma, serinletme ve toprak oluşumu gibi faydalardır. Bir okul bahçesi projesi yalnızca estetik değil, gölge, habitat ve öğrenme alanı üreten bir altyapı olarak değerlendirilebilir.'),
    ('Emisyon', 'Bir kaynaktan atmosfere salınan gaz veya parçacıklardır. Proje metninde emisyon azaltımını iddia etmek yerine hangi faaliyet, hangi başlangıç değeri ve hangi ölçüm yöntemiyle azaltılacağını gösterin.'),
    ('Emisyon faktörü', 'Bir faaliyet birimi başına oluşan tahmini emisyon miktarıdır. Örneğin enerji, ulaşım veya atık hesabında kullanılan faktörün kaynağı ve yılı belirtilmelidir; tahmin ile doğrudan ölçüm birbirine karıştırılmamalıdır.'),
    ('Gıda güvenliği', 'Gıdanın üretimden tüketime kadar fiziksel, kimyasal ve biyolojik tehlikelerden korunmuş, yeterli ve erişilebilir olması durumudur. İklim değişikliği sıcaklık, su kıtlığı, üretim ve depolama risklerini artırabildiği için güvenliği dayanıklılık planıyla birlikte ele alınır.'),
    ('Gıda kaybı', 'Gıdanın hasat, taşıma, depolama ve üretim aşamalarında tüketiciye ulaşmadan azalması veya niteliğini yitirmesidir. Kaynağı doğru belirlemek, çözümün tarlada mı, depoda mı, mutfakta mı kurulacağını gösterir.'),
    ('Gıda israfı', 'Tüketiciye, perakendeye veya yemek hizmetine ulaşmış yenilebilir gıdanın tüketilmeden atılmasıdır. Porsiyon, menü, satın alma, saklama ve davranış kararlarıyla ilişkilidir; okul pilotunda kilogram ve neden birlikte izlenmelidir.'),
    ('Gıda sistemi', 'Üretim, işleme, taşıma, pazarlama, tüketim ve atık yönetiminin oluşturduğu bütündür. Güçlü bir proje bir halkayı iyileştirirken diğer halkada yeni sorun üretmediğini açıklamalıdır.'),
    ('İklim adaleti', 'İklim krizinin sorumluluğu ve etkilerinin toplumlar arasında eşit olmadığını kabul eden yaklaşımdır. Çözüm tasarlarken kırılgan grupların riskini, söz hakkını ve faydaya erişimini görünür kılar.'),
    ('İklim direnci', 'Bir kişi, okul, şehir veya ekosistemin iklim şoklarına hazırlanma, etkilenme sırasında işlevini sürdürme ve sonrasında öğrenerek güçlenme kapasitesidir. Pilotun yalnızca iyi günde değil, sıcak hava veya su kesintisi gibi senaryolarda da çalışması test edilmelidir.'),
    ('İklim okuryazarlığı', 'İklim sistemini, değişimin nedenlerini ve sonuçlarını anlayıp güvenilir bilgiyle karar verme ve eyleme geçme becerisidir. Öğrencinin veri okuması kadar belirsizliği ve farklı çözüm seçeneklerini tartabilmesi de bu becerinin parçasıdır.'),
    ('Karbon ayak izi', 'Bir faaliyet, kişi veya ürünün doğrudan ve dolaylı sera gazı salımlarının karbondioksit eşdeğeriyle ifade edilmesidir. Kapsam, zaman aralığı, veri kaynağı ve hesap yöntemi yazılmadan verilen karbon sayısı karşılaştırılamaz.'),
    ('Karbon yutağı', 'Atmosferden karbonu emen ve depolayan doğal veya teknolojik sistemdir. Ormanlar, topraklar ve sulak alanlar doğal yutak örnekleridir; yutak iddiası yapılırken süreklilik, bakım ve izleme planı açıklanmalıdır.'),
    ('Karbon nötr', 'Belirli bir kapsamda salınan emisyonların azaltım ve doğrulanmış dengeleme adımlarıyla net olarak sıfırlanmasını hedefleyen durumdur. Önce gerçek azaltım, sonra dengeleme ilkesi korunmalıdır.'),
    ('Kırılgan grup', 'İklim risklerinden daha fazla etkilenebilen veya uyum kaynaklarına erişimi sınırlı olan gruptur. Yaş, sağlık, gelir, engellilik, mekân ve bakım sorumlulukları kırılganlığı etkileyebilir; proje planında mahremiyet korunmalıdır.'),
    ('Kuraklık', 'Yağışın uzun süre normalin altında kalması ve su talebiyle arzı arasındaki dengenin bozulmasıdır. Kuraklık planı yalnızca daha az su kullanmayı değil, gıda üretimi, sağlık, adil paylaşım ve erken uyarıyı da kapsar.'),
    ('Life cycle / yaşam döngüsü', 'Bir ürünün ham maddeden üretime, taşımaya, kullanıma ve kullanım sonrasına kadar bütün aşamalarının incelenmesidir. Bir çözümün bir aşamada kazandırıp başka bir aşamada daha fazla kaynak tüketip tüketmediğini görmeyi sağlar.'),
    ('Metan', 'Kısa vadede atmosferi güçlü biçimde ısıtan bir sera gazıdır. Organik atıkların oksijensiz ortamda parçalanması metan oluşturabilir; gıda israfını önlemek hem kaynak kaybını hem de atık kaynaklı emisyon riskini azaltır.'),
    ('Mikroplastik', 'Çevrede bulunan çok küçük plastik parçacıklardır. Gıda ambalajı, su ve atık çalışmaları yapılırken tek kullanımlık malzeme azaltımı, doğru veri ve sağlık iddialarında dikkatli kaynak kullanımı gerekir.'),
    ('Mutfak atığı', 'Yemek hazırlama ve tüketim sırasında ortaya çıkan organik veya ambalaj kaynaklı atıktır. Atığı kaynağında ayırmak, miktar kadar bileşimi de görmeyi ve kompost veya önleme kararını doğru vermeyi sağlar.'),
    ('OB8 Sürdürülebilirlik Okuryazarlığı', 'Sürdürülebilirlik sorunlarını anlama, sistemler arası ilişki kurma, kanıta dayalı karar verme, sorumluluk alma ve eylemi değerlendirme becerilerinin bütünüdür. İklim projesi bilgi, beceri, tutum ve eylemi görünür ürünlerle göstermelidir.'),
    ('Ölçülebilir etki', 'Bir projenin çevresel veya sosyal sonucunun başlangıç değeri, hedefi, zaman aralığı ve yöntemiyle izlenebilmesidir. “Farkındalık arttı” yerine test puanı, katılım oranı, kilogram atık veya litre su gibi göstergeler kullanılır.'),
    ('Önleme hiyerarşisi', 'Atık yönetiminde önce oluşumu önleme, sonra azaltma, yeniden kullanma, geri dönüştürme ve en son bertaraf etme sırasını ifade eder. Gıda için en değerli çözüm çoğu zaman atık oluşmadan önce planlama yapmaktır.'),
    ('Pilot uygulama', 'Bir fikrin sınırlı ölçekte, belirli süre ve göstergelerle denenmesidir. İyi pilotun hedef kitlesi, sorumlusu, takvimi, bütçesi, risk planı ve başarısızlıkta değiştirilecek varsayımı bulunur.'),
    ('Sera gazı', 'Atmosferde ısı tutarak küresel sıcaklık dengesini etkileyen gazlardır. Karbondioksit, metan ve diazot monoksit önemli örneklerdir; farklı gazlar karşılaştırılırken karbondioksit eşdeğeri kullanılır.'),
    ('Sürdürülebilir kalkınma', 'Bugünün ihtiyaçlarını karşılarken gelecek kuşakların ihtiyaçlarını karşılama kapasitesini azaltmayan kalkınma yaklaşımıdır. Çevre, toplum ve ekonomi birlikte değerlendirilmeden sürdürülebilirlik iddiası eksik kalır.'),
    ('Sürdürülebilir tarım', 'Toprağı, suyu, biyoçeşitliliği ve üreticinin geçimini uzun vadede koruyan tarım yaklaşımıdır. Verim kadar kaynak kullanımı, dayanıklılık, adalet ve yerel koşullara uyum da ölçülür.'),
    ('Su ayak izi', 'Bir ürün, kişi veya kurumun tükettiği suyun doğrudan ve üretim zincirindeki dolaylı bileşenlerini ifade eder. Hesapta ürünün kaynağı, üretim yöntemi ve veri belirsizliği açıkça yazılmalıdır.'),
    ('Su verimliliği', 'Aynı ihtiyacı daha az su ve daha az kayıpla karşılamaktır. Kaçakların giderilmesi, doğru zamanlama, uygun teknoloji ve davranış değişikliği birlikte ele alındığında kalıcı olur.'),
    ('Tedarik zinciri', 'Bir ürünün hammadde ve üreticiden tüketiciye ulaşana kadar geçtiği kişi, kurum, süreç ve taşıma ağıdır. Gıda projesi tedarik zincirindeki sıcaklık, mesafe, ambalaj ve kayıp noktalarını izleyebilir.'),
    ('Toprak organik maddesi', 'Bitki ve canlı kalıntılarından oluşan, toprağın su tutma, besin sağlama ve yapı özelliklerini etkileyen bileşendir. Artması toprak dayanıklılığını destekleyebilir; iddialar yerel ölçüm ve uzmanlıkla doğrulanmalıdır.'),
    ('Yaşam döngüsü analizi', 'Bir ürün veya hizmetin çevresel etkilerini tüm yaşam döngüsü boyunca sistematik olarak değerlendirme yöntemidir. Proje karşılaştırmalarında sınırların ve varsayımların aynı tutulmasını sağlar.'),
    ('Yeşil beceriler', 'Kaynak verimliliği, yenilenebilir enerji, döngüsel ekonomi, çevresel veri, ekolojik tasarım ve sürdürülebilir kararlarla ilgili bilgi ve uygulama becerileridir. Öğrenci projesi bu becerileri somut görevlerle göstermelidir.'),
]


class Command(BaseCommand):
    help = 'Populate the glossary with comprehensive climate, food, water, and project terms.'

    def handle(self, *args, **options):
        topics = list(Topic.objects.order_by('order'))
        for title, definition in TERMS:
            related_topic = None
            for topic in topics:
                if any(word in title.lower() or word in definition.lower() for word in topic.title.lower().split()[:2]):
                    related_topic = topic
                    break
            GlossaryTerm.objects.update_or_create(
                title=title,
                defaults={'definition': definition, 'related_topic': related_topic, 'is_published': True},
            )
        self.stdout.write(self.style.SUCCESS(f'Sözlük hazır: {GlossaryTerm.objects.filter(is_published=True).count()} terim.'))
