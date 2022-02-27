from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from shipper.models import Device

User = get_user_model()


class Command(BaseCommand):
    help = "Initializes a user with access to all enabled devices."

    def add_arguments(self, parser):
        parser.add_argument(
            "username", nargs=1, action="store", help="Username of user to be init"
        )

    def handle(self, *args, **options):
        self.stdout.write(
            "Initializing user {}. Do you want to continue? [y/N] ".format(
                options["username"][0]
            ),
            ending="",
        )

        if input().lower() == "y":
            self.stdout.write("Starting initialization...")

            # Make sure the user exists within the system
            try:
                user = User.objects.get(username=options["username"][0])
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR("The specified user does not exist!")
                )
                return

            # Add user to all existing devices
            devices = Device.objects.filter(status=True)

            for device in devices:
                self.stdout.write("Adding device {}... ".format(device), ending="")

                # Check if user is already a maintainer
                if user in device.maintainers.all():
                    self.stdout.write(self.style.WARNING("Skipped (already added)"))
                else:
                    device.maintainers.add(user)
                    self.stdout.write(self.style.SUCCESS("Added"))

            self.stdout.write(
                "The specified user has been added to all enabled devices!"
            )
        else:
            self.stdout.write("Exiting...")
            return
