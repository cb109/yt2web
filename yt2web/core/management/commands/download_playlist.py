import math
import os
import urllib.request

import pytube
from django.conf import settings
from django.core.management.base import BaseCommand
from yt2web.core.models import Playlist
from yt2web.core.models import Video
from django.core.files.base import File


def download_playlist_from_youtube_url(playlist_url):
    yt_playlist = pytube.Playlist(playlist_url)
    playlist, _ = Playlist.objects.get_or_create(
        url=playlist_url,
        title=yt_playlist.title,
    )
    if playlist.downloaded:
        return

    print(f"Downloading playlist {yt_playlist.title} ...")

    yt_videos = list(yt_playlist.videos)
    num_videos = len(yt_videos)
    num_digits = int(math.log10(num_videos)) + 1

    if not os.path.isdir(settings.MEDIA_ROOT):
        os.makedirs(os.path.normpath(settings.MEDIA_ROOT))

    for i, yt_video in enumerate(yt_videos):
        stream = yt_video.streams.get_audio_only()
        if not stream:
            print(f"No audio stream found for {yt_video.title}")
            continue

        n = str(i + 1).zfill(num_digits)
        print(f"[{n}/{num_videos}] Downloading {yt_video.title} ...")

        video_filepath = stream.download(output_path=settings.MEDIA_ROOT)
        video, _ = Video.objects.get_or_create(
            url=yt_video.watch_url,
            title=yt_video.title,
            audio_only=True,
        )
        playlist.videos.add(video)

        if video.downloaded:
            continue

        video_filename = os.path.basename(video_filepath)
        with open(video_filepath, "rb") as f:
            video.content_file.save(video_filename, File(f))

        thumbnail_url = yt_video.thumbnail_url
        if thumbnail_url:
            base, _ = os.path.splitext(video_filepath)
            image_filepath = base + ".jpg"
            print(f"  - Downloading thumbnail ...")
            urllib.request.urlretrieve(thumbnail_url, image_filepath)
            image_filename = os.path.basename(image_filepath)
            with open(image_filepath, "rb") as f:
                video.thumbnail_file.save(image_filename, File(f))

        video.downloaded = True
        video.save(update_fields=["downloaded"])

        print()

    playlist.downloaded = True
    playlist.save(update_fields=["downloaded"])
    print("Done")


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--url", action="store", default=None, dest="url")

    def handle(self, *args, **options):
        playlist_url = options.get("url")
        if playlist_url:
            download_playlist_from_youtube_url(playlist_url)
            return

        # Process any existing Playlists that are not yet downloaded.
        playlists = Playlist.objects.filter(downloaded=False)
        for playlist in playlists:
            download_playlist_from_youtube_url(playlist.url)
