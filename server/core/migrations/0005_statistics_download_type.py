# Generated by Django 4.2.4 on 2023-08-15 10:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_device_photo_device_photo_thumbhash"),
    ]

    operations = [
        migrations.AddField(
            model_name="statistics",
            name="download_type",
            field=models.CharField(
                choices=[("download", "Download"), ("update", "Updates (from OTA)")],
                default="download",
                max_length=8,
            ),
        ),
    ]
