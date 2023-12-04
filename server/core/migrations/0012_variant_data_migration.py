# Generated by Django 4.2.7 on 2023-11-24 01:53

from django.db import migrations


def update_build_variant(apps, _):
    Build = apps.get_model("core", "Build")
    Variant = apps.get_model("core", "Variant")

    for build in Build.objects.all():
        try:
            variant = Variant.objects.get(codename=build.variant_raw)
            build.variant = variant
            build.save()
        except Variant.DoesNotExist:
            # Handle the case where the variant doesn't exist
            raise Exception(
                f"A build referenced a variant {build.variant_raw} that "
                f"does not exist!"
            )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0011_build_variant"),
    ]

    operations = [migrations.RunPython(update_build_variant)]