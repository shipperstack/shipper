from django.contrib.auth.models import User
from django.core.management import BaseCommand

from shipper.models import Device


class Command(BaseCommand):
    help = "De-initializes a full user by removing access to all enabled devices."

    def add_arguments(self, parser):
        parser.add_argument('username', nargs=1, action='store', help='Username of user to be de-init')

    def handle(self, *args, **options):
        self.stdout.write("De-initializing user {}. Do you want to continue? [y/N] ".format(options['username'][0]),
                          ending='')

        if input().lower() == 'y':
            self.stdout.write("Starting removal...")

            # Make sure the user exists within the system
            try:
                user = User.objects.get(username=options['username'][0])
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR("The specified user does not exist!"))
                return

            # Remove user from all existing devices
            devices = Device.objects.filter(status=True)

            for device in devices:
                self.stdout.write("Removing device {}... ".format(device), ending='')

                # Check if user is already a maintainer
                if user not in device.maintainers.all():
                    self.stdout.write(self.style.WARNING("Skipped (already removed)"))
                else:
                    device.maintainers.remove(user)
                    self.stdout.write(self.style.SUCCESS("Removed"))

            self.stdout.write("The specified user has been removed from all enabled devices!")
        else:
            self.stdout.write("Exiting...")
            return
