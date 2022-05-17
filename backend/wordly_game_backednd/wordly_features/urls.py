from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import UserWordViewSet, ChallengeViewSet

v1_router = SimpleRouter()

v1_router.register('word', UserWordViewSet, basename='word')
v1_router.register('challenge', ChallengeViewSet, basename='challenge')

urlpatterns = [
    path('', include(v1_router.urls)),
]
