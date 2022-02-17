from django.shortcuts import render

from yt2web.core.models import Playlist


def playlists(request):
    songs = []
    for playlist in Playlist.objects.all().order_by("title"):
        for video in playlist.videos.all().order_by("title"):
            songs.append(
                {
                    "name": video.title,
                    "artist": "",
                    "album": "",
                    "url": video.content_file.url,
                    "cover_art_url": video.thumbnail_file.url,
                }
            )

    return render(request, "core/playlists.html", {"songs": songs})
