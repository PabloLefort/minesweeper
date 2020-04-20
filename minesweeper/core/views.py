from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from .exceptions import GameBoardDotOnMineError
from .models import Game
from .serializers import GameSerializer, GamePlaySerializer



class GameView(APIView):

    # authentication_classes = []

    def post(self, request):
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            #serializer.save(user=request.user)
            #serializer.save()
            game = Game.create(**serializer.validated_data)
            resp = {'id': game.id}
            return Response(resp, status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class GamePlayView(APIView):

    # authentication_classes = []

    def post(self, request, game_id=None):
        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return Response({'error': 'Invalid game id'}, status=HTTP_404_NOT_FOUND)
        serializer = GamePlaySerializer(data=request.data)
        if serializer.is_valid():
            x = serializer.validated_data.get('x')
            y = serializer.validated_data.get('y')
            try:
                game.play(x=x, y=y, is_flag=serializer.validated_data.get('flag'))
                resp = {}
                return Response(resp, status=HTTP_201_CREATED)
            except GameBoardDotOnMineError:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
