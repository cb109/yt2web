import math
import os
import urllib.request

import pytube
from django.conf import settings
from django.core.management.base import BaseCommand
from yt2web.core.models import Playlist
from yt2web.core.models import Video
from django.core.files.base import File


def download_playlist_from_youtube_url(
    playlist_url: str,
    verbose: bool = False,
    force: bool = False,
):
    yt_playlist = pytube.Playlist(playlist_url)
    playlist, created = Playlist.objects.get_or_create(url=playlist_url)

    if not created and playlist.title != yt_playlist.title:
        playlist.title = yt_playlist.title
        playlist.save(update_fields=["title"])

    if playlist.downloaded and not force:
        return

    if verbose:
        print(f"Downloading playlist ...")
        # print(f"Downloading playlist {yt_playlist.title} ...")

    yt_videos = list(yt_playlist.videos)
    num_videos = len(yt_videos)
    num_digits = int(math.log10(num_videos)) + 1

    if not os.path.isdir(settings.MEDIA_ROOT):
        os.makedirs(os.path.normpath(settings.MEDIA_ROOT))

    for i, yt_video in enumerate(reversed(yt_videos)):
        stream = yt_video.streams.get_audio_only()
        if not stream:
            # if verbose:
            #     print(f"No audio stream found for {yt_video.title}")
            continue

        n = str(i + 1).zfill(num_digits)

        if verbose:
            print(f"[{n}/{num_videos}] Downloading video ...")
            # print(f"[{n}/{num_videos}] Downloading {yt_video.title} ...")

        video, _ = Video.objects.get_or_create(
            url=yt_video.watch_url,
            audio_only=True,
        )
        if video.title != yt_video.title:
            video.title = yt_video.title
        if video.duration != yt_video.length:
            video.duration = yt_video.length
        video.save(update_fields=["title", "duration"])

        playlist.videos.add(video)

        if video.downloaded and video.content_file.name and video.thumbnail_file.name:
            continue

        temp_video_filepath = stream.download(output_path=settings.MEDIA_ROOT)
        video_filename = os.path.basename(temp_video_filepath)
        with open(temp_video_filepath, "rb") as f:
            video.content_file.save(video_filename, File(f))
        os.remove(temp_video_filepath)

        thumbnail_url = yt_video.thumbnail_url
        if thumbnail_url:
            base, _ = os.path.splitext(temp_video_filepath)
            temp_image_filepath = base + ".jpg"
            if verbose:
                print(f"  - Downloading thumbnail ...")
            urllib.request.urlretrieve(thumbnail_url, temp_image_filepath)
            image_filename = os.path.basename(temp_image_filepath)
            with open(temp_image_filepath, "rb") as f:
                video.thumbnail_file.save(image_filename, File(f))
            os.remove(temp_image_filepath)

        video.downloaded = True
        video.save(update_fields=["downloaded"])

        if verbose:
            print()

    if playlist.force_sync_on_next_download:
        playlist.force_sync_on_next_download = False
        playlist.save(update_fields=["force_sync_on_next_download"])

    if verbose:
        print("Done")


def download_unfinished_playlists(verbose: bool = False, force: bool = False):
    playlists = Playlist.objects.all()
    for playlist in playlists:
        if (
            playlist.downloaded
            and not playlist.force_sync_on_next_download
            and not force
        ):
            continue
        download_playlist_from_youtube_url(
            playlist.url,
            verbose=verbose,
            force=playlist.force_sync_on_next_download or force,
        )


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--url", action="store", default=None, dest="url")
        parser.add_argument(
            "--verbose", action="store_true", default=False, dest="verbose"
        )
        parser.add_argument("--force", action="store_true", default=False, dest="force")

    def handle(self, *args, **options):
        playlist_url = options.get("url")
        verbose = options.get("verbose")
        force = options.get("force")
        if playlist_url:
            download_playlist_from_youtube_url(
                playlist_url, verbose=verbose, force=force
            )
            return

        # Process any existing Playlists that are not yet downloaded.
        download_unfinished_playlists(verbose=verbose, force=force)
