# Generated by Django 3.2.13 on 2022-05-07 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shipper", "0037_alter_device_codename"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="statistics",
            options={"verbose_name": "statistic", "verbose_name_plural": "statistics"},
        ),
    ]
