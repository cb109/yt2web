# Generated by Django 4.0.2 on 2022-04-06 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_alter_playlist_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="playlist",
            name="force_sync_on_next_download",
            field=models.BooleanField(default=False),
        ),
    ]