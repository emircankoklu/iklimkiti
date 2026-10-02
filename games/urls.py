from django.urls import path

from games.views import (
    food_storage_game,
    game_detail,
    game_list,
    game_progress,
    game_submit,
    waste_detective_game,
)

urlpatterns = [
    path('', game_list, name='game_list'),
    path('ilerleme/', game_progress, name='game_progress'),
    path('gidani-dogru-sakla/', food_storage_game, name='food_storage_game'),
    path('israf-dedektifi/', waste_detective_game, name='waste_detective_game'),
    path('<slug>/submit/', game_submit, name='game_submit'),
    path('<slug>/', game_detail, name='game_detail'),
]
