import random

from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, response, status, viewsets, filters
from rest_framework.decorators import action

from .models import DayChallenge, UserWord, Words
from .serializers import DayChallengeSerializer, WordInputSerializer


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
        url_path='daychallenge',
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


class CustomizedListCreateViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """Base ViewSet for wordly.
    Allowed actions: `list`, `create`.
    Other actions returns HTTP 405.
    """
    filter_backends = (filters.SearchFilter)
    search_fields = ("word",)
    lookup_field = "word"
    permission_classes = [permissions.IsAuthenticated]


class UserWordViewSet(CustomizedListCreateViewSet):
    serializer_class = WordInputSerializer

    def get_queryset(self):
        """Return queryset for ViewSet."""
        task = get_object_or_404(
            DayChallenge, id=self.kwargs.get("task"))
        return task.user_word.select_related("player").all()

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        word = serializer.data['word']
        player = serializer.data['player']
        task = serializer.data['task']
        attempt = serializer.data['attempt']
        if attempt > 6:
            return response.Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        elif word == task:
            try:
                attempt += 1
                UserWord.objects.create(
                    word=word, player=player, task=task, attempt=attempt)
                return response.Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            except Exception as inst:
                raise Exception(f'Somthing wrong happended {inst}')
        else:
            try:
                attempt += 1
                UserWord.objects.create(
                    word=word, player=player, task=task, attempt=attempt)
                return response.Response(
                    serializer.data, status=status.HTTP_200_OK
                )
            except Exception as inst:
                raise Exception(f'Somthing wrong happended {inst}')
