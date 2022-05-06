from django.urls import include, path

from .views import RegistrationView

authpatterns = [
    path("auth/", RegistrationView.as_view(), name="auth_register"),
]

urlpatterns = [
    path("v1/", include(authpatterns)),
]
