import unicodedata

from django.db import models
from django.utils.text import slugify


def slugify_turkish(value):
    text = str(value)

    normalized = unicodedata.normalize('NFKD', text)
    ascii_text = ''.join(ch for ch in normalized if not unicodedata.combining(ch))

    for source, target in {
        'ı': 'i',
        'İ': 'I',
        'ğ': 'g',
        'Ğ': 'G',
        'ş': 's',
        'Ş': 'S',
        'ü': 'u',
        'Ü': 'U',
        'ö': 'o',
        'Ö': 'O',
        'ç': 'c',
        'Ç': 'C',
    }.items():
        ascii_text = ascii_text.replace(source, target)

    return slugify(ascii_text)


class Topic(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    theme = models.CharField(max_length=120, blank=True)
    description = models.TextField(blank=True)
    key_question = models.CharField(max_length=255, blank=True)
    action_text = models.CharField(max_length=255, blank=True)
    target_age = models.CharField(max_length=50, blank=True)
    estimated_duration_minutes = models.PositiveIntegerField(default=20)
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'title']
        indexes = [models.Index(fields=['is_published', 'title'])]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_turkish(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class LessonModule(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(blank=True)
    problem_statement = models.TextField(blank=True)
    real_life_example = models.TextField(blank=True)
    action_challenge = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_turkish(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class InformationCard(models.Model):
    CARD_TYPE_CHOICES = [
        ('fact', 'Gerçek'),
        ('warning', 'Uyarı'),
        ('action', 'Eylem'),
        ('question', 'Soru'),
        ('myth', 'Mit'),
        ('statistic', 'İstatistik'),
    ]

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='cards', null=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    card_type = models.CharField(max_length=20, choices=CARD_TYPE_CHOICES, default='fact')
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class QuestionAnswer(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='question_answers')
    question = models.CharField(max_length=255)
    answer = models.TextField()
    score_dimension = models.CharField(max_length=120, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Soru ve cevap'
        verbose_name_plural = 'Soru ve cevaplar'

    def __str__(self):
        return self.question


class VideoContent(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name='videos')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(blank=True)
    video_url = models.URLField(blank=True, default='')
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_turkish(self.title)
        super().save(*args, **kwargs)

    @staticmethod
    def get_youtube_embed_url(url):
        if not url:
            return ''
        video_id = ''
        if 'youtube.com/watch?v=' in url:
            video_id = url.split('watch?v=')[-1].split('&')[0]
        elif 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[-1].split('?')[0]
        elif 'youtube.com/embed/' in url:
            return url
        if not video_id:
            return url
        return f'https://www.youtube.com/embed/{video_id}'

    def __str__(self):
        return self.title


class MindMap(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='mind_maps')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='mindmaps/', blank=True, null=True)
    pdf_file = models.FileField(upload_to='mindmaps/pdf/', blank=True, null=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_turkish(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class MindMapNode(models.Model):
    mind_map = models.ForeignKey(MindMap, on_delete=models.CASCADE, related_name='nodes')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    position_x = models.IntegerField(default=0)
    position_y = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class GlossaryTerm(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    definition = models.TextField()
    related_topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name='glossary_terms')
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_turkish(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Source(models.Model):
    SOURCE_TYPE_CHOICES = [
        ('official', 'Resmî'),
        ('academic', 'Akademik'),
        ('educational', 'Eğitim'),
        ('international_organization', 'Uluslararası Kurum'),
        ('other', 'Diğer'),
    ]

    title = models.CharField(max_length=250)
    organization = models.CharField(max_length=200, blank=True)
    url = models.URLField(blank=True, default='')
    description = models.TextField(blank=True)
    published_date = models.DateField(null=True, blank=True)
    source_type = models.CharField(max_length=40, choices=SOURCE_TYPE_CHOICES, default='official')
    is_verified = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
