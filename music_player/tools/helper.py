from __future__ import unicode_literals
import os
import sys

import django
import mutagen.mp3

DEFAULT_MUSIC_LOCATION = os.path.normpath(r'../static/music_player/music/')
DEFAULT_MUSIC_FILE_EXTENSION = "mp3"

MP3_TAGS = {'artist': 'TPE1',
            'album_artist': 'TPE2',
            'year': 'TDRC',
            'genre': 'TCON',
            'release_type': 'TXXX:releasetype',
            'album': 'TALB',
            'disc_number': 'TPOS',
            'track_number': 'TRCK',
            'title': 'TIT2'}

FILE_EXTENSIONS = {'mp3': {'tags': MP3_TAGS, 'reader': mutagen.mp3.MP3}}


def prepare_django_models_for_importing():
    sys.path.append(r'../..')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mpwa.settings')
    django.setup()
    # import music_player.models


def find_extension(file_name):
    return file_name[file_name.rindex('.') + 1:]


def find_files(directories=(DEFAULT_MUSIC_LOCATION,), extensions=(DEFAULT_MUSIC_FILE_EXTENSION,)):
    """find_files finds all files with certain extensions in the given directories (including subdirectories)

    :rtype : generator of strings which represent file paths"""
    file_names = (os.path.join(root, file_name)
                  for directory in directories
                  for root, dirs, file_names in os.walk(directory)
                  for file_name in file_names
                  if find_extension(file_name) in extensions)

    return file_names


class TrackInformation(object):
    def __init__(self, track_path):
        self.track_location_on_disk = track_path[2:].replace("\\", "/")
        self.extension = find_extension(self.track_location_on_disk)

        try:
            self._tag_map = FILE_EXTENSIONS[self.extension]['tags']
            self._reader = FILE_EXTENSIONS[self.extension]['reader']
        except KeyError:
            raise ValueError(
                'File extension must be a valid music file extension. Your extension: ' + self.extension)

        self._mutagen_object = self._reader(track_path)

        self.artist = self._mutagen_object.get(self._tag_map['artist'], ('UNKNOWN ARTIST',))[0]
        self.album_artist = self._mutagen_object.get(self._tag_map['album_artist'], ('UNKNOWN ALBUM ARTIST',))[0]
        self.album_artist_location_on_disk = os.path.split(os.path.dirname(self.track_location_on_disk))[0]

        try:
            self.album_year = int(self._mutagen_object[self._tag_map['year']][0].text)
        except KeyError:
            self.album_year = 0

        self.album_name = self._mutagen_object.get(self._tag_map['album'], ('UNKNOWN ALBUM',))[0]
        self.album_release_type = self._mutagen_object.get(self._tag_map['release_type'], ('UNKNOWN',))[0].upper()
        self.album_genre = self._mutagen_object.get(self._tag_map['genre'], ('UNKNOWN',))[0]
        self.album_location_on_disk = os.path.split(self.track_location_on_disk)[0]
        self.album_cover = os.path.join(self.album_location_on_disk, 'folder.jpg')

        try:
            self.track_disc_number = int(self._mutagen_object[self._tag_map['disc_number']][0].split('/')[0])
        except KeyError:
            self.track_disc_number = 1

        try:
            self.track_number = int(self._mutagen_object[self._tag_map['track_number']][0].split('/')[0])
        except KeyError:
            self.track_number = 1

        self.track_title = self._mutagen_object.get(self._tag_map['title'], ('UNKNOWN TITLE',))[0]
        self.track_bit_rate = self._mutagen_object.info.bitrate
        self.track_duration = self._mutagen_object.info.length
        self.track_size_on_disk = os.path.getsize(track_path)


def cache_lookups(func):
    cache = {}

    def inner(*args, **kwargs):
        k = tuple(kwargs[key] for key in sorted(kwargs.keys()) if key != "defaults")

        if k in cache:
            return cache[k], False

        requested_object, created = func(*args, **kwargs)
        cache[k] = requested_object

        return requested_object, created

    return inner
