from django.core.management import BaseCommand

from shipper.models import Build
from shipper.tasks import generate_sha256


class Command(BaseCommand):
    help = "Calculates hashes for incomplete builds with interrupted processing."

    def handle(self, *args, **options):
        builds = Build.objects.filter(sha256sum__exact='')

        for build in builds:
            self.stdout.write("Queueing re-calculation of SHA256 hash for build {}...".format(build.file_name))
            generate_sha256.delay(build.id)

        self.stdout.write("All incomplete builds have been queued for processing. Please check the admin panel for "
                          "status updates.")
