from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Artist, Album, Track, Playlist, AuthUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


class AlbumInline(admin.StackedInline):
    model = Album
    extra = 0


class TrackInline(admin.StackedInline):
    model = Track
    extra = 0


class ArtistAdmin(admin.ModelAdmin):
    list_display = ('artist', 'votes', 'time_added')
    list_filter = ('time_added',)

    inlines = [AlbumInline]
    readonly_fields = ("time_added",)


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('album', 'artist', 'year', 'release_type', 'genre', 'disc_total', 'track_total', 'time_added')
    list_filter = ('release_type', 'year', 'genre', 'time_added')

    inlines = [TrackInline]
    readonly_fields = ("time_added",)


class TrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'album', 'artist', 'disc_number', 'track_number', 'play_count', 'time_added')
    list_filter = ('time_added',)

    readonly_fields = ("time_added",)


class AuthUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('username', 'is_active', 'is_staff', 'is_superuser', 'time_added')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'time_added')

    fieldsets = ((None, {'fields': ('username',
                                    'password',
                                    'is_active',
                                    'is_staff',
                                    'is_superuser',
                                    'time_added',
                                    'favorite_artists',
                                    'favorite_albums',
                                    'favorite_tracks',)}),)

    add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('username',
                                                              'password1',
                                                              'password2',
                                                              'is_staff',
                                                              'is_superuser',)}),)

    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ('favorite_artists', 'favorite_albums', 'favorite_tracks')
    readonly_fields = ("time_added",)


class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'votes', 'time_added')
    list_filter = ('created_by', 'time_added')

    readonly_fields = ('time_added',)
    filter_horizontal = ('tracks',)


admin.site.register(Artist, ArtistAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Track, TrackAdmin)
admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(AuthUser, AuthUserAdmin)
