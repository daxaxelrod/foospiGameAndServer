from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=255)
    path_to_sound_file = models.CharField(unique=True,max_length=255)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Game(models.Model):
    red_player = models.ForeignKey(Player, related_name='red_player')
    blue_player = models.ForeignKey(Player, related_name='blue_player')
    winner = models.CharField(max_length=4, choices=(("Red", "Red Won"), ("Blue","Blue Won")))
    final_score = models.CharField(max_length=20)
    epic_goal = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    duration = models.DecimalField(max_digits=15,decimal_places=3)

    def __str__(self):
        return 'Red: {0.red_player}. Blue: {0.blue_player}. Winner {0.winner}'.format(self)
