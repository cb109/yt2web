from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Video(BaseModel):
    url = models.CharField(max_length=512)
    title = models.CharField(max_length=256)
    content_file = models.FileField(
        null=True, blank=True, default=None, upload_to="videos"
    )
    thumbnail_file = models.FileField(
        null=True, blank=True, default=None, upload_to="thumbnails"
    )
    duration = models.PositiveIntegerField(default=0)
    audio_only = models.BooleanField(default=False)
    downloaded = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Playlist(BaseModel):
    url = models.CharField(max_length=512)
    title = models.CharField(max_length=256, default="", blank=True)
    videos = models.ManyToManyField("Video", blank=True, related_name="playlists")
    force_sync_on_next_download = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def downloaded(self):
        if not self.videos.exists():
            return False
        return all([video.downloaded for video in self.videos.all()])
