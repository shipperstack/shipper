from django.contrib.auth import get_user_model
from django.core.management import BaseCommand, call_command

from config import settings

User = get_user_model()


class Command(BaseCommand):
    help = "Runs commands to set up a developer demo environment."

    def handle(self, *args, **options):
        if not settings.DEBUG:
            self.stdout.write(
                self.style.ERROR(
                    "The server is running in production mode! Cannot set up a developer demo environment."
                )
            )
            return

        call_command("dev_add_demo_device", *args, **options)
        call_command("dev_add_demo_build", *args, **options)
