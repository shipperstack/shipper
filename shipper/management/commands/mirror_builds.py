from django.core.management import BaseCommand

from shipper.models import Build, MirrorServer
from shipper.tasks import mirror_build


class Command(BaseCommand):
    help = "Mirrors builds that haven't been mirrored yet."

    def handle(self, *args, **options):
        for build in Build.objects.exclude(is_mirrored=True):
            self.stdout.write("Backing up build {}...".format(build.file_name))
            mirror_build.delay(build.id)
            self.stdout.write("Queued backup for build {}!".format(build.file_name))

        self.stdout.write("Queued all incomplete builds. Please check the admin panel for status updates.")
