# Generated by Django 4.0.2 on 2022-02-26 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_remove_playlist_downloaded"),
    ]

    operations = [
        migrations.AlterField(
            model_name="playlist",
            name="title",
            field=models.CharField(blank=True, default="", max_length=256),
        ),
    ]
