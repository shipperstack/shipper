from django.core.management import BaseCommand
from core.models import Build
from server.core.tasks import check_build_exists_on_mirror


class Command(BaseCommand):
    help = (
        "Checks if each build is properly mirrored on each server and unsets "
        "the mirror if not."
    )

    def handle(self, *args, **options):
        missing_build_mirrors = 0
        for build in Build.objects.all():
            for mirror in build.mirrored_on.all():
                if check_build_exists_on_mirror(build, mirror):
                    self.stdout.write(
                        f"Successfully located build {build.file_name} on mirror {mirror}"
                    )
                else:
                    missing_build_mirrors += 1
                    self.stdout.write(
                        f"Warning: Build {build.file_name} does not exist on mirror {mirror}, unsetting... ",
                        ending="",
                    )
                    with transaction.atomic():
                        build.mirrored_on.remove(mirror)
                        build.save()
                    self.stdout.write("Unset.")

        self.stdout.write(
            f"Checked all mirrored builds. Found {missing_build_mirrors} missing builds on mirrors."
        )
