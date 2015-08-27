from __future__ import unicode_literals

import helper

helper.prepare_django_models_for_importing()
import music_player.models


def main():
    # Setting up models

    update_existing_artists = False
    artist_model = music_player.models.Artist
    artist_create_or_update_method = artist_model.objects.update_or_create if update_existing_artists else artist_model.objects.get_or_create

    update_existing_albums = False
    album_model = music_player.models.Album
    album_create_or_update_method = album_model.objects.update_or_create if update_existing_albums else album_model.objects.get_or_create

    update_existing_tracks = False
    track_model = music_player.models.Track
    track_create_or_update_method = track_model.objects.update_or_create if update_existing_tracks else track_model.objects.get_or_create

    # Memoize database lookups for artists, albums using the cache_lookups function from helper

    artist_create_or_update_method = helper.cache_lookups(artist_create_or_update_method)
    album_create_or_update_method = helper.cache_lookups(album_create_or_update_method)

    # Setting up track details

    dirs = (helper.DEFAULT_MUSIC_LOCATION,)
    exts = (helper.DEFAULT_MUSIC_FILE_EXTENSION,)

    track_files = helper.find_files(directories=dirs, extensions=exts)
    track_details = (helper.TrackInformation(track_file) for track_file in track_files)

    # Adding or updating the artist, album, track

    for track in track_details:
        artist, artist_created = artist_create_or_update_method(artist=track.album_artist,
                                                                defaults={
                                                                    'location_on_disk': track.album_artist_location_on_disk})

        album, album_created = album_create_or_update_method(artist=artist,
                                                             album=track.album_name,
                                                             defaults={'year': track.album_year,
                                                                       'release_type': track.album_release_type,
                                                                       'genre': track.album_genre,
                                                                       'location_on_disk': track.album_location_on_disk,
                                                                       'cover': track.album_cover})

        track, track_created = track_create_or_update_method(artist=artist,
                                                             album=album,
                                                             disc_number=track.track_disc_number,
                                                             track_number=track.track_number,
                                                             title=track.track_title,
                                                             defaults={'bit_rate': track.track_bit_rate,
                                                                       'duration': track.track_duration,
                                                                       'location_on_disk': track.track_location_on_disk,
                                                                       'size_on_disk': track.track_size_on_disk})


if __name__ == '__main__':
    main()
