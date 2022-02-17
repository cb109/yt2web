from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from yt2web.core.models import Playlist


@login_required
def playlist(request, playlist_id):
    songs = []
    playlist = get_object_or_404(Playlist, id=playlist_id)
    for video in playlist.videos.all().order_by("title"):
        songs.append(
            {
                "album": "",
                "artist": "",
                "cover_art_url": video.thumbnail_file.url,
                "duration": video.duration,
                "name": video.title,
                "url": video.content_file.url,
            }
        )

    return render(request, "core/playlists.html", {"songs": songs})
