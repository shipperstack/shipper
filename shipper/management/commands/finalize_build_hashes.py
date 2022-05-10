from django.core.management import BaseCommand

from shipper.models import Build
from shipper.tasks import generate_checksum


class Command(BaseCommand):
    help = "Calculates hashes for incomplete builds with interrupted processing."

    def handle(self, *args, **options):
        for build in [build for build in Build.objects.all() if not build.is_hashed()]:
            self.stdout.write(
                "Queueing re-calculation of SHA256 hash for build {}...".format(
                    build.file_name
                )
            )
            generate_checksum.delay(build.id)

        self.stdout.write(
            "All incomplete builds have been queued for processing. Please check the "
            "admin panel for status updates."
        )
