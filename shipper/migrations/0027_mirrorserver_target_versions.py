# Generated by Django 3.2.10 on 2022-02-02 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shipper", "0026_build_build_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="mirrorserver",
            name="target_versions",
            field=models.TextField(
                blank=True,
                help_text="Build versions to mirror to this server.<br>* will mirror all versions. Specify multiple versions using the delimiter set in settings.<br>For example, if your delimiter setting is -, then you would specify multiple versions like VERSION8-VERSION9. <br>Warning: this field does not take a version range! For example, VERSION7-VERSION9 will not mirror versions 7 through 9. Rather, it will only mirror versions 7 and 9 and leave out version 8.<br>Example: v12.8, v12.8-v12.9, *, ...",
                max_length=100,
                verbose_name="Target versions",
            ),
        ),
    ]
