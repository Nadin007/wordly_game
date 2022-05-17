from django.forms import ValidationError
from django.shortcuts import get_object_or_404

from rest_framework import serializers

from .models import DayChallenge, UserWord, Words
from user.serializers import CustomUserCreateSerializer


class WordSerializer(serializers.ModelSerializer):
    '''Serializer for word.'''
    class Meta:
        model = Words
        fields = ('id', 'word')


class ChallengeSerializer(serializers.ModelSerializer):
    '''Serializer for DayChallenge.'''
    player = CustomUserCreateSerializer(read_only=True)
    word = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = DayChallenge
        fields = ('id', 'word', 'date', 'player', 'is_active')

    def validate(self, data):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            raise ValidationError(
                'User should be authorised.'
            )
        is_exist = DayChallenge.objects.filter(player=request.user, is_active=True).exists()
        if request.method == 'POST':
            if is_exist:
                raise ValidationError(
                    'Challenge has been already created.'
                )
        if request.method == 'GET':
            if not is_exist:
                raise ValidationError(
                    'Callenge doesn`t exist.'
                )
        return super().validate(data)


class ChallengeWordSerializer(serializers.Serializer):
    word = WordSerializer(many=True)

    class Meta:
        fields = ("word",)


class WordInputSerializer(serializers.ModelSerializer):
    '''Serializer for UserWord'''
    player = serializers.ReadOnlyField(
        read_only=True
    )
    word = serializers.CharField(max_length=5, required=True)

    class Meta:
        model = UserWord
        fields = ("id", "word", "player", "attempt")

    def validate(self, attrs, **kwargs):
        """Checks that the player can enter only the word
        that is in the database.
        """

        if not self.context["request"].method == "POST":
            return attrs
        task = get_object_or_404(DayChallenge, is_active=True, player=self.context['request'].user)
        UserWord.objects.filter(task=task.id).all().count()
        word = self.initial_data.get('word')
        if not Words.objects.filter(word=word).exists():
            raise serializers.ValidationError(
                (
                    "There is not such word in the database."
                )
            )
        return attrs
