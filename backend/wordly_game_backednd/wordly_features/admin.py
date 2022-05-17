from django.contrib import admin

from .models import Words, DayChallenge


@admin.register(Words)
class WordAdmin(admin.ModelAdmin):
    list_display = ('id', 'word', )
    search_fields = ('word', )
    ordering = ('word', )


@admin.register(DayChallenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('player', 'is_active', 'date', 'word')
    search_fields = ('player', )
