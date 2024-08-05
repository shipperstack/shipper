from datetime import date

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from config import settings
from core.models import Device, Build, Variant

User = get_user_model()


class Command(BaseCommand):
    help = "Creates a demo build associated with the demo device in a developer environment."

    def handle(self, *args, **options):
        if not settings.DEBUG:
            self.stdout.write(
                self.style.ERROR(
                    "The server is running in production mode! The demo build was not created."
                )
            )
            return

        if Device.objects.filter(codename="demodevice").count() < 1:
            self.stdout.write(
                self.style.ERROR(
                    "The demo device to associate the build to was not found. Perhaps you want to try running "
                    "dev_add_demo_device first?"
                )
            )
            return

        demo_device = Device.objects.get(codename="demodevice")

        # Setup demo variant
        if Variant.objects.filter(codename="demovariant").count() < 1:
            self.stdout.write(
                self.style.NOTICE("Adding a demo variant to associate with the build.")
            )
            demo_variant = Variant(
                codename="demovariant", description="Variant for demo purposes"
            )
            demo_variant.save()
        else:
            demo_variant = Variant.objects.get(codename="demovariant")

        demo_build_file_name = "Bliss-v14-demodevice-OFFICIAL-demovariant-20200608"
        if Build.objects.filter(file_name=demo_build_file_name).count() >= 1:
            self.stdout.write(
                self.style.WARNING(
                    "The demo build already exists in the system. No changes were made."
                )
            )
            return

        demo_build = Build(
            device=demo_device,
            file_name=demo_build_file_name,
            size=857483855,
            version="v14",
            md5sum="d8e8fca2dc0f896fd7cb4cb0031ba249",
            sha256sum="b9566ebc192a4c27c72df19eae8a6eed6ea063226792e680fa0b2ede284e19f2",
            variant=demo_variant,
            build_date=date(2020, 6, 8),
            zip_file=f"{demo_device.codename}/{demo_build_file_name}.zip",
        )
        demo_build.save()

        self.stdout.write(self.style.SUCCESS("Successfully created the demo build!"))
