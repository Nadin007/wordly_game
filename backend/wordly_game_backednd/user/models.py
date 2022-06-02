import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):
    '''Model for user.'''
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        verbose_name='username', max_length=150,
        unique=True, help_text='Please enter up to 150 characters',
        validators=[username_validator],
        error_messages={
            'unique': 'User with the same username already exists'})
    user_token = models.UUIDField(
        verbose_name='user_token', unique=True,
        editable=False, default=uuid.uuid4, blank=False
    )
    REQUIRED_FIELDS = []
