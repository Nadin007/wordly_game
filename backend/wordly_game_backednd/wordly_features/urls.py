from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import ChallengeViewSet, UserStatView, UserWordViewSet

v1_router = SimpleRouter()

v1_router.register('word', UserWordViewSet, basename='word')
v1_router.register('challenge', ChallengeViewSet, basename='challenge')


urlpatterns = [
    path('', include(v1_router.urls)),
    path('stat/', UserStatView.as_view())
]
