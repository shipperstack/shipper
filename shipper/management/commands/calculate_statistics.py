import humanize
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from shipper.models import Build, Device

User = get_user_model()


class Command(BaseCommand):
    help = "Calculates total statistics for shipper."

    def handle(self, *args, **options):
        # Device/Maintainer Statistics
        devices = Device.objects.all()
        maintainers = User.objects.all()
        device_count = devices.count()
        maintainer_count = maintainers.count()
        enabled_devices_count = devices.filter(status=True).count()
        active_maintainers_count = maintainers.filter(is_active=True).count()
        self.stdout.write("{} devices maintained by {} maintainers."
                          .format(enabled_devices_count, active_maintainers_count))
        self.stdout.write("{} unsupported devices, {} inactive maintainers."
                          .format(device_count - enabled_devices_count, maintainer_count - active_maintainers_count))

        # Total Build Statistics
        builds = Build.objects.all()
        build_count = builds.count()
        total_size = 0

        for build in builds:
            total_size += build.size

        self.stdout.write("{} build files ({})".format(build_count, humanize.naturalsize(total_size)))

        # Build Variant Statistics
        vanilla_builds = builds.filter(variant="vanilla")
        vanilla_build_count = vanilla_builds.count()
        vanilla_total_size = 0
        gapps_builds = builds.filter(variant="gapps")
        gapps_build_count = gapps_builds.count()
        gapps_total_size = 0
        foss_builds = builds.filter(variant="foss")
        foss_build_count = foss_builds.count()
        foss_total_size = 0
        goapps_builds = builds.filter(variant="goapps")
        goapps_build_count = goapps_builds.count()
        goapps_total_size = 0

        for build in vanilla_builds:
            vanilla_total_size += build.size

        for build in gapps_builds:
            gapps_total_size += build.size

        for build in foss_builds:
            foss_total_size += build.size

        for build in goapps_builds:
            goapps_total_size += build.size

        self.stdout.write("Vanilla: {} builds ({})"
                          .format(vanilla_build_count, humanize.naturalsize(vanilla_total_size)))
        self.stdout.write("GApps: {} builds ({})"
                          .format(gapps_build_count, humanize.naturalsize(gapps_total_size)))
        self.stdout.write("FOSS: {} builds ({})"
                          .format(foss_build_count, humanize.naturalsize(foss_total_size)))
        self.stdout.write("GoApps: {} builds ({})"
                          .format(goapps_build_count, humanize.naturalsize(goapps_total_size)))
