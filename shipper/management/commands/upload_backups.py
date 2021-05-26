from django.core.management import BaseCommand

from shipper.models import Build, MirrorServer
from shipper.tasks import backup_build


class Command(BaseCommand):
    help = "Uploads builds that haven't been backed up yet."

    def handle(self, *args, **options):
        # Get all builds that are not mirrored on all enabled mirrors
        enabled_mirrors = MirrorServer.objects.filter(enabled=True)
        builds = Build.objects.exclude(mirrored_on=enabled_mirrors)

        for build in builds:
            self.stdout.write("Backing up build {}...".format(build.file_name))
            backup_build(build.id)
            self.stdout.write("Successfully backed up build {}!".format(build.file_name))

        self.stdout.write("Completed all backups.")
