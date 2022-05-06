from typing import Optional
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.backends import ModelBackend
from django.http import HttpRequest
from .models import User


class SettingsBackend(ModelBackend):
    def authenticate(self, request: Optional[HttpRequest]) -> Optional[AbstractBaseUser]:
        print('sdhjflkjasdhflsahdflsdhflshdflkjashdflahsdlfjahsdlfhasldfjh')
        usr_token = request.COOKIES.get('logged_in')
        print(usr_token)
        if usr_token:
            try:
                return User.objects.get(user_token=usr_token)
            except Exception:
                return None
        return None
