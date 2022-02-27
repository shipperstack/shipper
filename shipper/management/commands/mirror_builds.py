from django.core.management import BaseCommand
from shipper.models import Build
from shipper.tasks import mirror_build


class Command(BaseCommand):
    help = "Mirrors builds that haven't been mirrored yet."

    def handle(self, *args, **options):
        for build in [
            build for build in Build.objects.all() if not build.is_mirrored()
        ]:
            mirror_build.delay(build.id)
            self.stdout.write(f"Queued backup for build {build.file_name}!")

        self.stdout.write(
            "Queued all incomplete builds. Please check the admin panel for status updates."
        )
