# Generated by Django 3.1.6 on 2021-02-15 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shipper", "0003_auto_20201121_0555"),
    ]

    operations = [
        migrations.AlterField(
            model_name="build",
            name="file_name",
            field=models.TextField(
                help_text="Example: 'Bliss-v14-bullhead-OFFICIAL-gapps-20200608",
                max_length=500,
                unique=True,
            ),
        ),
    ]
