from django.db import models


class BuildFeature(models.Model):
    name = models.CharField(
        max_length=100, help_text="Name of the feature. Shown to users."
    )
    description = models.CharField(
        max_length=500, help_text="Description of the feature. Shown to users."
    )
