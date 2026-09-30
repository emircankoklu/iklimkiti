from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from learning.models import GlossaryTerm, MindMap, QuestionAnswer, Topic, VideoContent


def topic_list(request):
    queryset = Topic.objects.filter(is_published=True)
    query = request.GET.get('q', '').strip()
    if query:
        queryset = queryset.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(theme__icontains=query))
    return render(request, 'learning/topic_list.html', {'topics': queryset, 'query': query})


def topic_detail(request, slug):
    topic = get_object_or_404(Topic, slug=slug, is_published=True)
    modules = topic.modules.filter(is_published=True)
    cards = topic.cards.filter(is_published=True)[:8]
    videos = topic.videos.filter(is_published=True)[:4]
    maps = topic.mind_maps.filter(is_published=True)[:4]
    question_answers = topic.question_answers.filter(is_published=True)
    return render(request, 'learning/topic_detail.html', {'topic': topic, 'modules': modules, 'cards': cards, 'videos': videos, 'maps': maps, 'question_answers': question_answers})


def module_detail(request, slug):
    from learning.models import LessonModule

    module = get_object_or_404(LessonModule, slug=slug, is_published=True)
    return render(request, 'learning/module_detail.html', {'module': module, 'topic': module.topic})


def video_list(request):
    queryset = VideoContent.objects.filter(is_published=True)
    query = request.GET.get('q', '').strip()
    if query:
        queryset = queryset.filter(Q(title__icontains=query) | Q(description__icontains=query))
    return render(request, 'learning/video_list.html', {'videos': queryset, 'query': query})


def video_detail(request, slug):
    video = get_object_or_404(VideoContent, slug=slug, is_published=True)
    return render(request, 'learning/video_detail.html', {'video': video, 'embed_url': VideoContent.get_youtube_embed_url(video.video_url)})


def mind_map_list(request):
    queryset = MindMap.objects.filter(is_published=True)
    query = request.GET.get('q', '').strip()
    if query:
        queryset = queryset.filter(Q(title__icontains=query) | Q(description__icontains=query))
    return render(request, 'learning/mind_map_list.html', {'mind_maps': queryset, 'query': query})


def mind_map_detail(request, slug):
    mind_map = get_object_or_404(MindMap, slug=slug, is_published=True)
    return render(request, 'learning/mind_map_detail.html', {'mind_map': mind_map, 'nodes': mind_map.nodes.all()})


def glossary_list(request):
    queryset = GlossaryTerm.objects.filter(is_published=True)
    query = request.GET.get('q', '').strip()
    if query:
        queryset = queryset.filter(Q(title__icontains=query) | Q(definition__icontains=query))
    letter = request.GET.get('letter', '').strip()
    if letter:
        queryset = queryset.filter(title__istartswith=letter)
    return render(request, 'learning/glossary_list.html', {'terms': queryset, 'query': query, 'letter': letter})


def glossary_detail(request, slug):
    term = get_object_or_404(GlossaryTerm, slug=slug, is_published=True)
    return render(request, 'learning/glossary_detail.html', {'term': term})
