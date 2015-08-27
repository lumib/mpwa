from __future__ import unicode_literals

from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils.translation import gettext as _
from django.utils.encoding import python_2_unicode_compatible


# ----------------------------------------------------------------------------------------------------------------------
# Artist, Album, Track, models


@python_2_unicode_compatible
class Artist(models.Model):
    artist = models.CharField(_('name'), max_length=1024, blank=False)
    bio = models.TextField(_('short biography'), blank=True)
    cover = models.CharField(_('photography'), max_length=1024, blank=True)
    location_on_disk = models.CharField(_("location on disk"), max_length=1024, blank=True)
    votes = models.IntegerField("number of votes", blank=True, default=0)
    time_added = models.DateTimeField(_('added on'), auto_now_add=True, editable=False)

    def __str__(self):
        return self.artist

    class Meta:
        verbose_name = "artist"
        verbose_name_plural = "artists"
        ordering = ['artist']
        unique_together = (('artist',))


@python_2_unicode_compatible
class Album(models.Model):
    artist = models.ForeignKey(Artist)
    year = models.IntegerField(_('year'), blank=True, null=True)
    album = models.CharField(_('album'), max_length=1024)
    disc_total = models.IntegerField(_('number of discs'), default=1, blank=True, null=True)
    track_total = models.IntegerField(_('number of tracks'), default=0, blank=True, null=True)
    release_type = models.CharField(_('album type'), max_length=20, blank=True)
    genre = models.CharField(_('genre'), max_length=128, blank=True)
    duration = models.IntegerField(_('duration'), default=0, blank=True)
    size_on_disk = models.IntegerField(_('size on disk'), default=0, blank=True)
    location_on_disk = models.CharField(_('location on disk'), max_length=1024, blank=True)
    cover = models.CharField(_('cover'), max_length=1024, blank=True)
    votes = models.IntegerField("number of votes", blank=True, default=0)
    time_added = models.DateTimeField(_('added on'), auto_now_add=True, editable=False)

    def __str__(self):
        return "{} - {} - {} - {} - {} - {}".format(self.artist,
                                                    self.year,
                                                    self.album,
                                                    self.track_total,
                                                    self.release_type,
                                                    self.genre,
                                                    self.duration,
                                                    self.size_on_disk)

    class Meta:
        verbose_name = "album"
        verbose_name_plural = "albums"
        ordering = ['artist', 'year', 'release_type']
        unique_together = (('artist', 'year', 'album', 'release_type',))


@python_2_unicode_compatible
class Track(models.Model):
    artist = models.ForeignKey(Artist)
    album = models.ForeignKey(Album)
    disc_number = models.IntegerField(_('disc number'), default=0, blank=True, null=True)
    track_number = models.IntegerField(_('track number'), default=0, blank=True, null=True)
    title = models.CharField(_('title'), max_length=1024)
    bit_rate = models.CharField(_('bitrate'), max_length=16, blank=True)
    duration = models.IntegerField(_("duration"), blank=True)
    formatted_duration = models.CharField(_("formatted duration"), blank=True, max_length=256)
    location_on_disk = models.CharField(_('location'), max_length=1024, blank=True)
    size_on_disk = models.IntegerField(_("size on disk"), blank=True)
    play_count = models.IntegerField("play count", blank=True, default=0)
    time_added = models.DateTimeField(_('added on'), auto_now_add=True, editable=False)

    def __str__(self):
        return "{}/CD{} - {}. {}".format(self.album,
                                         self.disc_number,
                                         self.track_number,
                                         self.title)

    class Meta:
        verbose_name = "track"
        verbose_name_plural = "tracks"
        ordering = ['album__artist', 'album', 'disc_number', 'track_number']
        unique_together = (('album', 'disc_number', 'track_number', 'title'))

    def save(self, *args, **kwargs):
        minutes, seconds = divmod(int(self.duration), 60)
        self.formatted_duration = "{}:{:0>2d}".format(minutes, seconds)

        self.size_on_disk = self.size_on_disk

        super(Track, self).save(*args, **kwargs)


# ----------------------------------------------------------------------------------------------------------------------
# Users


class AuthUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('The given username must be set')
        user = self.model(username=username)
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


@python_2_unicode_compatible
class AuthUser(AbstractBaseUser, PermissionsMixin):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z.]*$', message="Only alphanumeric characters and . allowed.")

    username = models.CharField(_("username"), max_length=20, unique=True, validators=[alphanumeric])
    favorite_artists = models.ManyToManyField(Artist, related_name="favorited_by", blank=True)
    favorite_albums = models.ManyToManyField(Album, related_name="favorited_by", blank=True)
    favorite_tracks = models.ManyToManyField(Track, related_name="favorited_by", blank=True)
    time_added = models.DateTimeField(_("added on"), auto_now_add=True, editable=False)
    is_active = models.BooleanField(_("is active"), default=True, null=False)
    is_staff = models.BooleanField(_("is staff"), default=False, null=False)

    objects = AuthUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username


# ----------------------------------------------------------------------------------------------------------------------
# Playlist model


@python_2_unicode_compatible
class Playlist(models.Model):
    created_by = models.ForeignKey(AuthUser)
    name = models.CharField(_("playlist name"), max_length=256, blank=False)
    tracks = models.ManyToManyField(Track, related_name="track_of", blank=True)
    votes = models.IntegerField("number of votes", blank=True, default=0)
    time_added = models.DateTimeField(_('added on'), auto_now_add=True, editable=False)

    class Meta:
        verbose_name = "playlist"
        verbose_name_plural = "playlists"

    def __str__(self):
        return "Playlist by: {}".format(self.created_by)


# ----------------------------------------------------------------------------------------------------------------------
# Signals

@receiver(post_save, sender=Track)
def on_track_creation(sender, instance, created, **kwargs):
    if created:
        instance.album.track_total = models.F('track_total') + 1
        instance.album.disc_total = max(instance.album.disc_total, instance.disc_number)
        instance.album.duration = models.F('duration') + instance.duration
        instance.album.size_on_disk = models.F('size_on_disk') + instance.size_on_disk
        instance.album.save()


@receiver(pre_delete, sender=Track)
def on_track_deletion(sender, instance, **kwargs):
    instance.album.track_total = models.F('track_total') - 1
    instance.album.duration = models.F('duration') - instance.duration
    instance.album.size_on_disk = models.F('size_on_disk') - instance.size_on_disk
    instance.album.save()
