from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404

from .models import Artist, Album, Track


def index(request):
    return render(request, "music_player/home.html")


def artists(request):
    template = "music_player/_artists.html" if request.is_ajax() else "music_player/artists.html"

    all_artists = Artist.objects.all().values("id", "artist")
    context = {'artists': all_artists}

    response = render(request, template, context)
    response['Expires'] = '-1'

    return response


def artist_id(request, id):
    template = "music_player/_artist.html" if request.is_ajax() else "music_player/artist.html"

    artist = get_object_or_404(Artist, pk=id)
    artist_albums = artist.album_set.all().values("id", "cover", "release_type", "year", "album")
    context = {"artist": artist, "albums": artist_albums}

    response = render(request, template, context)
    response['Expires'] = '-1'

    return response


def albums(request):
    template = "music_player/_albums.html" if request.is_ajax() else "music_player/albums.html"

    all_albums = Album.objects.all().values("id", "artist__artist", "year", "album")
    context = {'albums': all_albums}

    response = render(request, template, context)
    response['Expires'] = '-1'

    return response


def album_id(request, id):
    template = "music_player/_album.html" if request.is_ajax() else "music_player/album.html"

    album = get_object_or_404(Album.objects.select_related("artist"), id=id)
    album_tracks = album.track_set.all().values("id", "location_on_disk", "track_number", "title", "artist__artist",
                                                "formatted_duration")
    context = {"album": album, "tracks": album_tracks}

    response = render(request, template, context)
    response['Expires'] = '-1'

    return response


def tracks(request):
    template = "music_player/_tracks.html" if request.is_ajax() else "music_player/tracks.html"

    all_tracks = Track.objects.all().values("id", "location_on_disk", "title", "artist__artist", "formatted_duration")
    context = {"tracks": all_tracks}

    response = render(request, template, context)
    response['Expires'] = '-1'

    return response


def track_id(request, id):
    template = "music_player/_track.html" if request.is_ajax() else "music_player/track.html"

    track = get_object_or_404(Track, pk=id)
    context = {"track": track}

    response = render(request, template, context)
    response['Expires'] = '-1'

    return response


def playlists(request):
    # template = "music_player/_playlists.html" if request.is_ajax() else "music_player/playlists.html"
    template = "music_player/_base.html"

    response = render(request, template)
    response['Expires'] = '-1'

    return response


def playlist_id(request, id):
    # template = "music_player/_playlist.html" if request.is_ajax() else "music_player/playlist.html"
    template = "music_player/_base.html"

    response = render(request, template)
    response['Expires'] = '-1'

    return response


def radios(request):
    # template = "music_player/_radios.html" if request.is_ajax() else "music_player/radios.html"
    template = "music_player/_base.html"

    response = render(request, template)
    response['Expires'] = '-1'

    return response
