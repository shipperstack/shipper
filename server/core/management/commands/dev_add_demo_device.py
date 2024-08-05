from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from config import settings
from core.models import Device

User = get_user_model()


class Command(BaseCommand):
    help = "Creates a demo device in a developer environment."

    def handle(self, *args, **options):
        if not settings.DEBUG:
            self.stdout.write(
                self.style.ERROR(
                    "The server is running in production mode! The demo device was not created."
                )
            )
            return

        demo_device = Device(
            name="Demo Device",
            codename="demodevice",
            manufacturer="ACME",
            status=True,
        )
        demo_device.save()

        self.stdout.write(self.style.SUCCESS("Successfully created the demo device!"))
