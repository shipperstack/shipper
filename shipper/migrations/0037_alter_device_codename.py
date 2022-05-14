# Generated by Django 3.2.13 on 2022-05-04 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shipper", "0036_build_md5sum"),
    ]

    operations = [
        migrations.AlterField(
            model_name="device",
            name="codename",
            field=models.TextField(
                help_text="Example: 'bullhead', 'angler'", max_length=20, unique=True
            ),
        ),
    ]