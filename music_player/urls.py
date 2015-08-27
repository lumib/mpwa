from __future__ import unicode_literals

from django.conf.urls import url

from .views import index, artists, artist_id, albums, album_id, tracks, track_id, playlists, playlist_id, radios

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^artists/$', artists, name='artists'),
    url(r'^artists/(?P<id>[0-9]+)/$', artist_id, name='artist_id'),
    url(r'^albums/$', albums, name='albums'),
    url(r'^albums/(?P<id>[0-9]+)/$', album_id, name='album_id'),
    url(r'^tracks/$', tracks, name='tracks'),
    url(r'^tracks/(?P<id>[0-9]+)/$', track_id, name='track_id'),
    url(r'^playlists/$', playlists, name='playlists'),
    url(r'^playlists/(?P<id>[0-9]+)/$', playlist_id, name='playlist_id'),
    url(r'^radios/$', radios, name='radios'),
]
