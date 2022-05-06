from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import UserWordViewSet, day_word

v1_router = SimpleRouter()

v1_router.register('word', UserWordViewSet, basename='word')

urlpatterns = [
    path('', include(v1_router.urls)),
    path('', day_word, name='challenge')
]
