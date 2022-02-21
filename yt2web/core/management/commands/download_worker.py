import time

from django.core.management.base import BaseCommand
from yt2web.core.management.commands.download_playlist import (
    download_unfinished_playlists,
)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--seconds", action="store", default=5, dest="seconds")

    def handle(self, *args, **options):
        seconds = options["seconds"]
        while True:
            download_unfinished_playlists()
            time.sleep(seconds)
