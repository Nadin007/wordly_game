from ast import IsNot
from imp import source_from_cache
from rest_framework import serializers
from .models import DayChallenge, Words, UserWord
from datetime import datetime


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
        source_from_cache="user_token",
        read_only=True
    )
    task = serializers.ReadOnlyField(
        source=DayChallenge.objects.filter(
            date=datetime.now().strftime('%Y-%m-%d'))
    )

    class Meta:
        model = UserWord
        fields = ("id", "word", "task", "player", "attempt")

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
