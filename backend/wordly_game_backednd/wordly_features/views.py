import random

from django.shortcuts import get_object_or_404

from .serializers import DayChallengeSerializer, WordInputSerializer
from .models import Words, DayChallenge
from rest_framework import generics, permissions, response, status
from rest_framework.decorators import action


def random_word():
    length = len(Words.objects.all()) - 1
    index_word = random.randint(0, length)
    return Words.objects.get(id=index_word)


def del_word(self, request, pk):
    word = get_object_or_404(DayChallenge, user=request.user, recipe=pk)
    word.delete()
    return response.Response(
        status=status.HTTP_204_NO_CONTENT)


def daily_word():
    while True:
        try:
            pk_word = random_word()
            day_challenge = get_object_or_404(Words, pk=pk_word)
            DayChallenge.objects.create(word=day_challenge)
        except Exception as inst:
            raise Exception(f'Somthing wrong happended {inst}')


@action(detail=True, methods=['POST', 'DELETE'],
        url_path='day_challenge',
        permission_classes=[permissions.IsAdminUser],)
def day_word(request, pk):
    if request.method == 'POST':
        serializer = DayChallengeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(
                serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        return del_word(request, pk)


class UserWordViewSet(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = WordInputSerializer

    def perform_create(self, serializer):
        word = serializer.data['word']
        player = serializer.data['player']
        task = 
        attempt = 

        return super().perform_create(serializer)


