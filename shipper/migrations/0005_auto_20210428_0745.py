# Generated by Django 3.2 on 2021-04-28 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipper', '0004_auto_20210215_0804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='build',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='device',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
