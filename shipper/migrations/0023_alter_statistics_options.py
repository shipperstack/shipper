# Generated by Django 3.2.5 on 2021-07-12 09:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shipper", "0022_statistics"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="statistics",
            options={"verbose_name": "statistic", "verbose_name_plural": "statistics"},
        ),
    ]
