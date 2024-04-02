from django.core.management import BaseCommand
from core.models import Build

class Command(BaseCommand):
    help = "Checks if build files exist on the server and unsets the build file field if not."

    def handle(self, *args, **options):
        for build in Build.objects.all():
            if bool(build.zip_file) and build.zip_file.storage.exists(build.zip_file.name):
                self.stdout.write(f"Build {build.file_name} is available in the system, not unsetting.")
            else:
                self.stdout.write(f"Build {build.file_name} does not exist, unsetting... ", ending='')
                build.zip_file.delete(save=True)
                self.stdout.write(f"Unset.")

        self.stdout.write("All missing builds have been cleared from the system.")
