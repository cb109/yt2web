from django.contrib.auth.decorators import login_required
import datetime

from django.shortcuts import get_object_or_404
from django.shortcuts import render

from yt2web.core.models import Playlist


def to_mm_ss_string(seconds: int) -> str:
    return str(datetime.timedelta(seconds=seconds)).replace("0:", "", 1)


@login_required
def playlist(request, playlist_id: int):
    songs = []
    playlist = get_object_or_404(Playlist, id=playlist_id)
    for video in playlist.videos.all().order_by("title"):
        songs.append(
            {
                "album": "",
                "artist": "",
                "cover_art_url": video.thumbnail_file.url,
                "duration": to_mm_ss_string(video.duration),
                "name": video.title,
                "url": video.content_file.url,
            }
        )

    return render(request, "core/playlists.html", {"songs": songs})
