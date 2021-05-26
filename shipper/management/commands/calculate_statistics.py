import humanize
from django.contrib.auth.models import User
from django.core.management import BaseCommand

from shipper.models import Build, Device


class Command(BaseCommand):
    help = "Calculates total statistics for shipper."

    def handle(self, *args, **options):
        builds = Build.objects.all()
        device_count = Device.objects.all().count()
        build_count = builds.count()
        maintainer_count = User.objects.all().count()

        total_size = 0

        for build in builds:
            total_size += build.size

        self.stdout.write("There are currently {} builds taking up {} storage.".format(build_count,
                                                                                       humanize.naturalsize(total_size))
                          )
        self.stdout.write("There are currently {} devices registered.".format(device_count))
        self.stdout.write("There are currently {} maintainers registered.".format(maintainer_count))
