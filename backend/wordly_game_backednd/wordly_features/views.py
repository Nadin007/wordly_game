from rest_framework.decorators import action
import random

from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, response, status, viewsets, filters

from .models import DayChallenge, UserWord, Words
from .serializers import ChallengeSerializer, WordInputSerializer, ChallengeWordSerializer


def random_word():
    length = Words.objects.all().count()
    index_word = random.randint(1, length)
    return Words.objects.get(id=index_word)


def del_word(self, request, pk):
    word = get_object_or_404(DayChallenge, user=request.user, recipe=pk)
    word.delete()
    return response.Response(
        status=status.HTTP_204_NO_CONTENT)


def get_word():
    try:
        pk_word = random_word()
        return get_object_or_404(Words, id=pk_word.id)
    except Exception as inst:
        raise Exception(f'Somthing wrong happended {inst}')


def rewiever(word, task):
    couner = 0
    ls = list(map(lambda el: str(el), task))
    result = [-1] * 5
    for el in word:
        if el == ls[couner]:
            result[couner] = 1
            ls[couner] = '_'
        couner += 1
    couner = 0
    for el in word:
        if result[couner] != 1:
            try:
                index_value = ls.index(el)
                ls[index_value] = '_'
                result[couner] = 0
            except ValueError:
                index_value = -1
        couner += 1
    return result


class CustomizedGetPostDeleteViewSet(mixins.DestroyModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Base ViewSet for challenge.
    Allowed actions: `retrieve`, `create`, `delete`.
    Other actions returns HTTP 405.
    """
    permission_classes = [permissions.IsAuthenticated]


class ChallengeViewSet(CustomizedGetPostDeleteViewSet):
    serializer_class = ChallengeSerializer
    queryset = DayChallenge.objects.all()

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return response.Response(
                request, status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(is_active=True, word=get_word(), player=request.user)
            return response.Response(
                serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        methods=['GET', ],
        url_path='current',)
    def get_challenge(self, request):
        serializer = ChallengeSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        task = get_object_or_404(DayChallenge, is_active=True, player=request.user.id)
        words = Words.objects.filter(user_word__task=task)
        data = {
            'word': words
        }
        response_data = ChallengeWordSerializer(data, context={'request': request})
        return response.Response(
            response_data.data, status=status.HTTP_200_OK)


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

    def list(self, request, *args, **kwargs):
        print(request.user)
        task = get_object_or_404(
            DayChallenge, is_active=True, player=request.user.id)
        words = Words.objects.filter(user_word__task=task)
        data = {
            'word': words
        }
        response_data = ChallengeWordSerializer(data=data, context={'request': request})
        response_data.is_valid(raise_exception=True)
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        print('11111111111')
        word = serializer.data['word']
        player = self.request.user
        print(word, player)
        task = DayChallenge.objects.filter(is_active=True, player=player)[0]
        print(task)
        attempt = UserWord.objects.filter(task=task.id).count()
        print(attempt)
        if attempt > 6:
            return response.Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        elif word == task.word:
            try:
                attempt += 1
                UserWord.objects.create(
                    word=word, player=player, task=task.word, attempt=attempt)
                data = {'response': [1, 1, 1, 1, 1]}
                return response.Response(
                    data, status=status.HTTP_201_CREATED
                )
            except Exception as inst:
                raise Exception(f'Somthing wrong happended {inst}')
        else:
            try:
                attempt += 1
                UserWord.objects.create(
                    word=word, player=player, task=task.word, attempt=attempt)
                for el in word:
                    pass
                return response.Response(
                    serializer.data, status=status.HTTP_200_OK
                )
            except Exception as inst:
                raise Exception(f'Somthing wrong happended {inst}')
