from rest_framework import serializers

from . import models


class PlayerSerializer(serializers.ModelSerializer):
    # games = serializers.PrimaryKeyRelatedField(
    #     many=True,
    #     read_only=True,
    # )

    class Meta:
        fields = (
            'id',
            'name',
            'path_to_sound_file',
            'wins',
            'losses',

        )
        model = models.Player


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        # extra_kwargs = {
        #     'email': {'write_only': True}
        # }
        fields = (
            'id',
            'red_player',
            'blue_player',
            'winner',
            'final_score',
            'epic_goal',
            'created_at',
            'duration',
        )
        model = models.Game

    # you can add validators by def validate_epic_goal(self,value):
            #return value if all good
        # else raise a validation error
