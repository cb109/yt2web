from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from yt2web.core.models import Playlist
from yt2web.core.models import Video


class BaseModelAdmin(admin.ModelAdmin):
    save_as = True
    save_on_top = True


class PlaylistAdmin(BaseModelAdmin):
    list_display = (
        "title_or_url",
        "num_videos",
        "player_link",
        "youtube_link",
        "downloaded",
        "force_sync_on_next_download",
        "created_at",
        "updated_at",
    )
    filter_horizontal = ("videos",)
    readonly_fields = ("player_link", "youtube_link", "downloaded")

    def title_or_url(self, playlist):
        return playlist.title or playlist.url

    def downloaded(self, playlist):
        return playlist.downloaded

    downloaded.boolean = True

    def num_videos(self, playlist):
        return playlist.videos.count()

    @mark_safe
    def player_link(self, playlist):
        if not playlist.id:
            return ""
        url = reverse("playlist", args=(playlist.id,))
        return f"<a href='{url}'>Go to Player</a>"

    @mark_safe
    def youtube_link(self, playlist):
        if not playlist.url:
            return ""
        return f"<a href='{playlist.url}'>Go to YouTube</a>"


class VideoAdmin(BaseModelAdmin):
    list_display = (
        "title",
        "thumbnail",
        "player",
        "duration",
        "youtube_link",
        "downloaded",
        "created_at",
        "updated_at",
    )

    list_filter = ("playlists", "downloaded")
    readonly_fields = ("player", "youtube_link")

    @mark_safe
    def thumbnail(self, video):
        if not video.thumbnail_file.name:
            return ""
        return f"<img src='{video.thumbnail_file.url}' style='max-width: 200px'>"

    @mark_safe
    def player(self, video):
        if not video.content_file.name:
            return ""
        return f"<audio controls src='{video.content_file.url}'>"

    @mark_safe
    def youtube_link(self, video):
        return f"<a href='{video.url}'>Go to YouTube</a>"


admin.site.site_header = "yt2web"
admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(Video, VideoAdmin)
