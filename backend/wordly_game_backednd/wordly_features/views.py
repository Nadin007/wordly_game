import random

from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, response, status, viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView

from .models import DayChallenge, UserWord, Words
from .queries import biult_stat
from .serializers import (ChallengeSerializer, ChallengeWordSerializer,
                          WordInputSerializer)


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


class UserStatView(APIView):

    @action(
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        methods=['GET', ], )
    def get(self, request):
        print(request.user.id)
        data = biult_stat(request.user.id)
        print(data)
        return response.Response(data=data, status=status.HTTP_200_OK)


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
            data = {'status': "New challenge has been created"}
            return response.Response(
                data, status=status.HTTP_201_CREATED)
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

    lookup_field = "word"
    permission_classes = [permissions.IsAuthenticated]


class UserWordViewSet(CustomizedListCreateViewSet):
    serializer_class = WordInputSerializer

    def list(self, request, *args, **kwargs):
        task = get_object_or_404(
            DayChallenge, is_active=True, player=request.user.id)
        words = Words.objects.filter(user_word__task=task)
        data = {
            'word': words
        }
        response_data = ChallengeWordSerializer(data=data, context={'request': request})
        response_data.is_valid(raise_exception=True)
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        word = Words.objects.get(word=serializer.data['word'])
        player = self.request.user

        task = DayChallenge.objects.get(is_active=True, player=player)
        attempt = UserWord.objects.filter(task=task.id).count()
        if attempt > 6:
            return response.Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        if word == task.word:
            try:
                attempt += 1
                UserWord.objects.create(
                    word=word, task=task, attempt=attempt)
                task.is_active = False
                task.save()
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
                    word=word, task=task, attempt=attempt)
                data = {'response': rewiever(word.word, task.word.word)}
                if attempt == 6:
                    task.is_active = False
                    task.save()
                return response.Response(
                    data, status=status.HTTP_200_OK
                )
            except Exception as inst:
                raise Exception(f'Somthing wrong happended {inst}')
