from django.core.management import BaseCommand

from shipper.models import Build
from shipper.tasks import backup_build


class Command(BaseCommand):
    help = "Uploads builds that haven't been backed up yet."

    def handle(self, *args, **options):
        builds = Build.objects.filter(backed_up=False)

        for build in builds:
            self.stdout.write("Backing up build {}...".format(build.file_name))
            backup_build(build.id)
            self.stdout.write("Successfully backed up build {}!".format(build.file_name))

        self.stdout.write("Completed all backups.")
