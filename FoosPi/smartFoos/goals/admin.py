from django.contrib import admin

# Register your models here.
from . import models


class GameAdmin(admin.ModelAdmin):
    
    search_fields = ['red_player','blue_player','final_score']

    list_filter = ['red_player','blue_player']
    
    list_display = [
        'red_player',
        'blue_player',
        'winner',
        'final_score',
        'duration',
        ]

admin.site.register(models.Player)
admin.site.register(models.Game, GameAdmin)
