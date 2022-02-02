# Generated by Django 3.2.10 on 2022-02-02 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipper', '0028_alter_mirrorserver_target_versions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mirrorserver',
            name='target_versions',
            field=models.TextField(blank=True, help_text='Build versions to mirror to this server.<br>* will mirror all versions. Specify multiple versions on each line.<br>Warning: wildcarding is not supported. For example, v12.* will not work.<br>Example: v12.8, *, ...', max_length=100, verbose_name='Target versions'),
        ),
    ]