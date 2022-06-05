import uuid

from rest_framework import generics, permissions, response, status

from .models import User
from .serializers import CustomUserCreateSerializer


class RegistrationView(generics.CreateAPIView):
    """ Create a new user."""

    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomUserCreateSerializer

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return response.Response(status=status.HTTP_200_OK)

        try:
            user_token = uuid.uuid4()
            username = user_token
            User.objects.create(user_token=user_token, username=username)
        except Exception as intr:
            raise Exception(f'User cannot be created {intr}')

        obj_response = response.Response(data=user_token, status=status.HTTP_201_CREATED)
        obj_response.set_cookie('logged_in', user_token, max_age=300000, httponly=True, samesite='Lax')
        return obj_response
