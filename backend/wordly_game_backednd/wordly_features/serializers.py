from rest_framework import serializers
from .models import Words, UserWord


class WordSerializer(serializers.ModelSerializer):
    '''Serializer for word.'''
    class Meta:
        model = Words
        fields = ('id', 'word', 'is_active')


class WordInputSerializer(serializers.ModelSerializer):
    '''Serializer for UserWord'''
    player = serializers.SlugRelatedField(
        slug_field="user_token",
        read_only=True,
    )

    class Meta:
        model = UserWord
        fields = ("id", "word", "player")

    def validate(self, attrs):
        """Check that the player can enter only the word
        that is in the database.
        """
        if not self.context["request"].method == "POST":
            return attrs
        if Words.objects.filter(
                word=self.context["view"].kwargs.get("word")).exists():
            raise serializers.ValidationError(
                (
                    "There is not such word in the database."
                )
            )
        return attrs