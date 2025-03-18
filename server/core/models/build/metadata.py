from django.db import models

from core.models import Build


class Metadata(models.Model):
    build = models.ForeignKey(Build, on_delete=models.CASCADE, db_index=True)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)