from rest_framework import serializers

from .models import Game


class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        fields = ['status', 'won', 'id']


class GamePlaySerializer(serializers.Serializer):
    flag = serializers.BooleanField(required=False, default=False)
    x = serializers.IntegerField(required=True)
    y = serializers.IntegerField(required=True)
