from django.urls import path

from games.views import game_detail, game_list, game_progress, game_submit

urlpatterns = [
    path('', game_list, name='game_list'),
    path('ilerleme/', game_progress, name='game_progress'),
    path('<slug>/submit/', game_submit, name='game_submit'),
    path('<slug>/', game_detail, name='game_detail'),
]
