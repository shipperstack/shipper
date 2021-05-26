import humanize
from django.core.management import BaseCommand

from shipper.models import Build, Device


class Command(BaseCommand):
    help = "Calculates total statistics for shipper."

    def handle(self, *args, **options):
        builds = Build.objects.all()
        devices = Device.objects.all()

        total_size = 0
        build_count = 0
        device_count = 0

        for build in builds:
            total_size += build.size
            build_count += 1

        for _ in devices:
            device_count += 1

        self.stdout.write("{} builds for {} devices taking up {} storage.".format(build_count, device_count,
                                                                                  humanize.naturalsize(total_size)))
