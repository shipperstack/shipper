from django.db import models


class Statistics(models.Model):
    time = models.DateTimeField(auto_now_add=True, editable=False)
    build = models.ForeignKey(
        "Build", related_name="build_stats", on_delete=models.CASCADE
    )
    ip = models.GenericIPAddressField(unpack_ipv4=True)

    DOWNLOAD_TYPES = (("download", "Download"), ("update", "Updates (from OTA)"))
    download_type = models.CharField(
        max_length=8, default="download", choices=DOWNLOAD_TYPES
    )

    class Meta:
        verbose_name = "statistic"
        verbose_name_plural = "statistics"

    def get_device(self):
        return self.build.device
