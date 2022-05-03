from .models import Score
from rest_framework import generics, permissions
from rest_framework.decorators import action


class ScoreViewSet(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):

        return super().post(request)
