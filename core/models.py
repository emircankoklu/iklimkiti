from django.db import models
from django.conf import settings


class ChatPromptLog(models.Model):
	STATUS_CHOICES = [
		('received', 'Alındı'),
		('blocked', 'Engellendi'),
		('answered', 'Yanıtlandı'),
	]

	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_prompt_logs')
	prompt = models.TextField()
	status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='received')
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']
		verbose_name = 'Asistan prompt kaydı'
		verbose_name_plural = 'Asistan prompt kayıtları'

	def __str__(self):
		return f'{self.user} - {self.created_at:%Y-%m-%d %H:%M}'


class HomePageContent(models.Model):
	hero_tag = models.CharField(max_length=120, default='Gıda güvenliği ve iklim eğitimi')
	hero_title = models.CharField(max_length=255, default='Gıdanın yolculuğunu öğren, geleceği birlikte koru.')
	hero_description = models.TextField(default='İklimKiti ile gıda güvenliği, sürdürülebilir yaşam ve iklim değişikliği hakkında öğren, keşfet ve oyunlarla kendini geliştir.')
	relationship_title = models.CharField(max_length=200, default='Gıda ve iklim ilişkisi')
	relationship_lead = models.CharField(max_length=255, default='Yediğimiz her gıdanın arkasında su, toprak, enerji, emek ve taşıma süreçleri bulunur.')
	relationship_body = models.TextField(blank=True, default='Bu süreçleri tanımak, hem kendi seçimlerimizi hem de gezegenimizin geleceğini daha bilinçli değerlendirmemize yardımcı olur.')
	assistant_title = models.CharField(max_length=200, default='İklimKiti Asistanı')
	assistant_description = models.TextField(default='Gıda güvenliği, gıda israfı, su kaynakları ve sürdürülebilir yaşam hakkında kısa sorular sorabilirsiniz.')
	is_active = models.BooleanField(default=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = 'Ana sayfa içeriği'
		verbose_name_plural = 'Ana sayfa içeriği'

	def save(self, *args, **kwargs):
		self.pk = 1
		super().save(*args, **kwargs)

	def __str__(self):
		return 'Ana sayfa ayarları'


class HomeAction(models.Model):
	content = models.ForeignKey(HomePageContent, on_delete=models.CASCADE, related_name='actions')
	title = models.CharField(max_length=120)
	description = models.TextField()
	order = models.PositiveIntegerField(default=0)
	is_published = models.BooleanField(default=True)

	class Meta:
		ordering = ['order', 'id']
		verbose_name = 'Ana sayfa eylem önerisi'
		verbose_name_plural = 'Ana sayfa eylem önerileri'

	def __str__(self):
		return self.title


class IdeathonGuide(models.Model):
	title = models.CharField(max_length=220, default='Gıda ve eğitim için iklim çözümü stüdyosu')
	subtitle = models.CharField(max_length=255, default='COP31 Maarif İklim İdeathonu için kanıttan prototipe uzanan çalışma alanı')
	introduction = models.TextField()
	source_url = models.URLField(blank=True)
	is_published = models.BooleanField(default=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = 'COP31 proje rehberi'
		verbose_name_plural = 'COP31 proje rehberi'

	def save(self, *args, **kwargs):
		self.pk = 1
		super().save(*args, **kwargs)

	def __str__(self):
		return self.title


class GuideSection(models.Model):
	CATEGORY_CHOICES = [
		('evidence', 'Kanıt ve problem'),
		('innovation', 'Yenilik ve çözüm'),
		('education', 'Eğitim ve OB8'),
		('food', 'Gıda ve su'),
		('implementation', 'Uygulanabilirlik'),
		('impact', 'Ölçülebilir etki'),
		('submission', 'Başvuru hazırlığı'),
		('ethics', 'Etik ve yaygınlaştırma'),
	]

	guide = models.ForeignKey(IdeathonGuide, on_delete=models.CASCADE, related_name='sections')
	title = models.CharField(max_length=220)
	eyebrow = models.CharField(max_length=100, blank=True)
	body = models.TextField()
	prompt = models.TextField(blank=True)
	score_weight = models.PositiveIntegerField(default=0)
	order = models.PositiveIntegerField(default=0)
	is_published = models.BooleanField(default=True)

	class Meta:
		ordering = ['order', 'id']
		verbose_name = 'Rehber bölümü'
		verbose_name_plural = 'Rehber bölümleri'

	def __str__(self):
		return self.title
