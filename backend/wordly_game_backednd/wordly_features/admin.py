from django.contrib import admin

from .models import Words, DayChallenge, UserWord


@admin.register(Words)
class WordAdmin(admin.ModelAdmin):
    list_display = ('id', 'word', )
    search_fields = ('word', )
    ordering = ('word', )


@admin.register(DayChallenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('player', 'is_active', 'date', 'word')
    search_fields = ('player', )


@admin.register(UserWord)
class UserWordAdmin(admin.ModelAdmin):
    fields = ('attempt', 'word', 'task',)
    list_display = ('attempt', 'word', 'task', )
    search_fields = ('task', )
