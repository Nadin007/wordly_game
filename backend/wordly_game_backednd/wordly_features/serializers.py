from ast import IsNot
from datetime import datetime

from rest_framework import serializers

from .models import DayChallenge, UserWord, Words


class WordSerializer(serializers.ModelSerializer):
    '''Serializer for word.'''
    class Meta:
        model = Words
        fields = ('id', 'word', 'is_active')


class DayChallengeSerializer(serializers.ModelSerializer):
    '''Serializer for DayChallenge.'''
    class Meta:
        model = DayChallenge
        fields = ('id', 'word', 'date')


class WordInputSerializer(serializers.ModelSerializer):
    '''Serializer for UserWord'''
    player = serializers.ReadOnlyField(
        read_only=True
    )
    task = serializers.ReadOnlyField(
        source=DayChallenge.objects.filter(
            date=datetime.now().strftime('%Y-%m-%d'))
    )
    attempt = serializers.SerializerMethodField('get_attempt')

    class Meta:
        model = UserWord
        fields = ("id", "word", "task", "player", "attempt")

    def get_attempt(self, instance):
        return UserWord.objects.filter(
            player=instance.player, task=instance.task).all().count()

    def validate(self, attrs):
        """Checks that the player can enter only the word
        that is in the database.
        """
        if not self.context["request"].method == "POST":
            return attrs
        if IsNot(Words.objects.filter(
                word=self.context["view"].kwargs.get("word")).exists()):
            raise serializers.ValidationError(
                (
                    "There is not such word in the database."
                )
            )
        return attrs
