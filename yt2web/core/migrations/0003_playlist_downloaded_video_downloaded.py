# Generated by Django 4.0.2 on 2022-02-17 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_playlist_created_at_playlist_updated_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='downloaded',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='video',
            name='downloaded',
            field=models.BooleanField(default=False),
        ),
    ]
