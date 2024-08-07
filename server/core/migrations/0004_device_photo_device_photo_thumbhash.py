# Generated by Django 4.2.3 on 2023-07-14 05:18

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_rename_photo_device_photo_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="device",
            name="photo",
            field=models.FileField(
                blank=True,
                help_text="Photo file of device. If blank, the server will try and download the photo in the "
                "`photo_url` field.",
                upload_to=core.models.Device.get_image_upload_path,
            ),
        ),
        migrations.AddField(
            model_name="device",
            name="photo_thumbhash",
            field=models.TextField(
                blank=True,
                help_text="Thumbhash of device photo. If blank, the server will try and regenerate it from the photo "
                "in the `photo` field.",
            ),
        ),
    ]
