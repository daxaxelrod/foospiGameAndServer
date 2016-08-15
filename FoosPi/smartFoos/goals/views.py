from django.shortcuts import render, get_object_or_404

from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from . import models
from . import serializers
import datetime
# Create your views here.

from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from django.db.models import Q


from . import models
from . import serializers


class ListCreatePlayer(generics.ListCreateAPIView):
    queryset = models.Player.objects.all()
    serializer_class = serializers.PlayerSerializer


class RetrieveUpdateDestroyPlayer(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Player.objects.all()
    serializer_class = serializers.PlayerSerializer


class ListCreateGame(generics.ListCreateAPIView):
    queryset = models.Game.objects.all()
    serializer_class = serializers.GameSerializer

    # refactor into allows to filter based on 2 name
    def get_queryset(self):
        if self.kwargs.get('player_id') is not None:
            return self.queryset.filter(Q(blue_player_id=self.kwargs.get('player_id')) | Q(red_player_id=self.kwargs.get('player_id')))
        else:
            return self.queryset.all()

    def perform_create(self, serializer):
        print("______")
        print(self.request.data['duration'])
        try:
            epic_goal = bool(self.request.data['epic_goal'])
        except:
            epic_goal = False

        print("______")
        red = models.Player.objects.filter(id=self.request.data['red_player']).get()
        blue = models.Player.objects.filter(id=self.request.data['blue_player']).get()
        # blue_player = models.Player.objects.filter(id=self.request.data['blue_player'])
        models.Game.objects.create(red_player=red,
                                   blue_player=blue,
                                   winner=self.request.data['winner'],
                                   final_score=str(self.request.data['final_score']),
                                   epic_goal=epic_goal,
                                   duration=self.request.data['duration']
                                   # duration's timedelta isnt showing up in the model
                                   # duration=datetime.timedelta(seconds=int(str(self.request.data["duration"])[2:])),
                                   )
        if "Red" in self.request.data['winner']:
            #red won
            red.wins += 1
            red.save()
            blue.losses +=1
            blue.save()
        else:
            #blue won
            blue.wins += 1
            blue.save()
            red.losses += 1
            red.save()
        
        # serializer.save(game)


class RetrieveUpdateDestroyGame(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Game.objects.all()
    serializer_class = serializers.GameSerializer

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(),
            player_id=self.kwargs.get('player_pk'),
            pk=self.kwargs.get('pk')
        )


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        else:
            if request.method == 'DELETE':
                return False


class PlayerViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsSuperUser,
        permissions.DjangoModelPermissions,
    )
    queryset = models.Player.objects.all()
    serializer_class = serializers.PlayerSerializer

    @detail_route(methods=['get'])
    def reviews(self, request, pk=None):
        self.pagination_class.page_size = 1
        reviews = models.Game.objects.filter(course_id=pk)

        page = self.paginate_queryset(reviews)

        if page is not None:
            serializer = serializers.GameSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.GameSerializer(
            reviews, many=True)
        return Response(serializer.data)


class GameViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = models.Game.objects.all()
    serializer_class = serializers.GameSerializer
