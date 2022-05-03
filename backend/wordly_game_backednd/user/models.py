from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    '''Model for user.'''
    user_token = models.UUIDField(
        verbose_name='user_token', unique=True,
        editable=False, default=uuid.uuid4, blank=False
    )
