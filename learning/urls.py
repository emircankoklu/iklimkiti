from django.urls import path

from learning.views import (
    glossary_detail,
    glossary_list,
    mind_map_detail,
    mind_map_list,
    module_detail,
    topic_detail,
    topic_list,
    video_detail,
    video_list,
)

urlpatterns = [
    path('', topic_list, name='topic_list'),
    path('modul/<slug>/', module_detail, name='module_detail'),
    path('video/', video_list, name='video_list'),
    path('video/<slug>/', video_detail, name='video_detail'),
    path('zihin-haritalari/', mind_map_list, name='mind_map_list'),
    path('zihin-haritalari/<slug>/', mind_map_detail, name='mind_map_detail'),
    path('sozluk/', glossary_list, name='glossary_list'),
    path('sozluk/<slug>/', glossary_detail, name='glossary_detail'),
    path('<slug>/', topic_detail, name='topic_detail'),
]
