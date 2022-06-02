from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import constraints
from django.db.models.functions import Lower

from user.models import User

NEW_FORMAT = '%Y-%m-%d %H:%M'


class Words(models.Model):
    ''''Model for words bank.'''
    word = models.CharField(
        verbose_name='word value', max_length=5,
        unique=True
    )

    class Meta:
        ordering = [Lower('word')]
        verbose_name = 'Word'
        verbose_name_plural = 'Words'

    def __str__(self) -> str:
        return self.word


class DayChallenge(models.Model):
    word = models.ForeignKey(
        Words, on_delete=models.CASCADE,
        verbose_name='entered word', related_name='challenge')
    date = models.DateTimeField(
        verbose_name='date of adding', default=datetime.now)
    STRING_METHOD_MESSAGE = (
        'word: {word.word}, date:{date}'
    )
    is_active = models.BooleanField(
        verbose_name='Is word in use',
        default=False
    )
    player = models.ForeignKey(
        User, verbose_name='id_user',
        on_delete=models.CASCADE, related_name='challenge')

    class Meta:
        ordering = ['-date']
        verbose_name = 'DayChallenge'
        verbose_name_plural = 'DayChallenges'
        constraints = [constraints.UniqueConstraint(
            fields=['player', 'word'], name='unique task to player')]

    def __str__(self) -> str:
        return self.STRING_METHOD_MESSAGE.format(
            player=self.player,
            word=self.word,
            is_active=self.is_active,
            date=datetime.strftime(self.date, NEW_FORMAT)
        )


class UserWord(models.Model):
    '''Model that connects Word with User.'''
    word = models.ForeignKey(
        Words, on_delete=models.CASCADE,
        verbose_name='entered word', related_name='user_word', max_length=5)
    task = models.ForeignKey(
        DayChallenge,
        verbose_name='hidden word', related_name='user_word',
        on_delete=models.CASCADE, max_length=5)
    attempt = models.PositiveIntegerField(
        verbose_name='attempt number', default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(6)]
    )

    class Meta:
        verbose_name = 'UserWord'
        verbose_name_plural = 'UserWords'
        constraints = [
            constraints.UniqueConstraint(
                fields=['word', 'task'],
                name='prevention doubling'
            )
        ]

    def __str__(self) -> str:
        return f'{self.task}, - {self.word}'
