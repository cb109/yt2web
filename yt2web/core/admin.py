from django.contrib import admin
from django.utils.safestring import mark_safe

from yt2web.core.models import Playlist
from yt2web.core.models import Video


class BaseModelAdmin(admin.ModelAdmin):
    save_as = True
    save_on_top = True


class PlaylistAdmin(BaseModelAdmin):
    list_display = (
        "title",
        "num_videos",
        "link",
        "downloaded",
        "created_at",
        "updated_at",
    )
    filter_horizontal = ("videos",)

    def num_videos(self, playlist):
        return playlist.videos.count()

    @mark_safe
    def link(self, playlist):
        if not playlist.url:
            return ""
        return f"<a href='{playlist.url}'>Watch on YouTube</a>"


class VideoAdmin(BaseModelAdmin):
    list_display = (
        "title",
        "thumbnail",
        "player",
        "duration",
        "link",
        "downloaded",
        "created_at",
        "updated_at",
    )

    @mark_safe
    def thumbnail(self, video):
        if not video.thumbnail_file.name:
            return ""
        return f"<img src='{video.thumbnail_file.url}' style='max-width: 200px'>"

    @mark_safe
    def player(self, video):
        if not video.content_file.name:
            return ""
        return f"<audio preload='auto' controls src='{video.content_file.url}'>"

    @mark_safe
    def link(self, video):
        return f"<a href='{video.url}'>Watch on YouTube</a>"


admin.site.site_header = "yt2web"
admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(Video, VideoAdmin)
