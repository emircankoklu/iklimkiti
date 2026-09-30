from django.test import TestCase

from learning.models import GlossaryTerm, LessonModule, Topic, VideoContent


class LearningModelTests(TestCase):
    def test_topic_slug_is_generated(self):
        topic = Topic.objects.create(title='Gıda Güvenliği ve İklim', slug='')
        self.assertEqual(topic.slug, 'gida-guvenligi-ve-iklim')

    def test_module_belongs_to_topic(self):
        topic = Topic.objects.create(title='Sürdürülebilir Tarım', slug='surdurulebilir-tarim')
        module = LessonModule.objects.create(topic=topic, title='Toprak ve Su', slug='toprak-ve-su')
        self.assertEqual(module.topic, topic)

    def test_unpublished_content_is_hidden(self):
        topic = Topic.objects.create(title='Gıda İsrafı', slug='gida-israfi', is_published=False)
        self.assertFalse(Topic.objects.filter(is_published=True).filter(pk=topic.pk).exists())

    def test_video_url_can_be_blank(self):
        video = VideoContent.objects.create(title='Video', slug='video', is_published=True, video_url='')
        self.assertEqual(video.video_url, '')

    def test_glossary_slug_is_generated(self):
        term = GlossaryTerm.objects.create(title='Su Ayak İzi', slug='')
        self.assertEqual(term.slug, 'su-ayak-izi')
