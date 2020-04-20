from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import GameView, GamePlayView

urlpatterns = [
    path('game/', GameView.as_view()),
    path('game/<int:game_id>/play', GamePlayView.as_view()),
]
