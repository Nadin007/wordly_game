from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import constraints
from django.db.models.functions import Lower

from user.models import User


class Words(models.Model):
    ''''Model for words bank.'''
    word = models.CharField(
        verbose_name='word value', max_length=5,
        unique=True
    )
    is_active = models.BooleanField(
        verbose_name='Is word in use',
        default=False
    )

    class Meta:
        ordering = [Lower('word')]
        verbose_name = 'Word'
        verbose_name_plural = 'Words'

    def __str__(self) -> str:
        return self.word


class DayChallenge(models.Model):
    word = models.ForeignKey(
        Words, on_delete=models.SET_DEFAULT, default='Deleted_word',
        verbose_name='entered word', related_name='challenge')
    date = models.DateTimeField(
        verbose_name='date of adding', default=datetime.now)
    STRING_METHOD_MESSAGE = (
        'word: {word.word}, date:{date}'
    )

    class Meta:
        ordering = ['-date']
        verbose_name = 'DayChallenge'
        verbose_name_plural = 'DayChallenges'

    def __str__(self) -> str:
        return self.STRING_METHOD_MESSAGE.format(
            word=self.word,
            date=self.date
        )


class UserWord(models.Model):
    '''Model that connects Word with User.'''
    word = models.ForeignKey(
        Words, on_delete=models.SET_DEFAULT, default='Deleted_word',
        verbose_name='entered word_id', related_name='user_word')
    task = models.ForeignKey(
        DayChallenge,
        verbose_name='hidden word_id', related_name='user_word',
        on_delete=models.SET_DEFAULT, default='Deleted_task')
    player = models.ForeignKey(
        User, verbose_name='id_user',
        on_delete=models.CASCADE, related_name='user_word')
    attempt = models.PositiveIntegerField(
        verbose_name='user\'s tryes', default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(6)]
    )

    class Meta:
        verbose_name = 'UserWord'
        verbose_name_plural = 'UserWords'
        constraints = [
            constraints.UniqueConstraint(
                fields=['word', 'task', 'player'],
                name='prevention doubling'
            )
        ]

    def __str__(self) -> str:
        return f'{self.player}, - {self.word}'
