from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.ListCreatePlayer.as_view(), name='player_list'),
    url(r'(?P<pk>\d+)/$',
        views.RetrieveUpdateDestroyPlayer.as_view(),
        name='game_detail'),
    url(r'^(?P<player_pk>\d+)/games/$',
        views.ListCreateGame.as_view(),
        name='game_list'),
    url(r'^(?P<player_pk>\d+)/games/(?P<pk>\d+)/$',
        views.RetrieveUpdateDestroyGame.as_view(),
        name='game_detail'),
    url(r'^games/$', views.ListCreateGame.as_view())
]
