from django.db import models


class Variant(models.Model):
    codename = models.TextField(
        max_length=10,
        help_text="Codename of the variant<br>Example: 'vanilla', 'gapps')",
        unique=True,
    )
    description = models.TextField(
        max_length=30,
        help_text="Description of the variant<br>Example: 'Vanilla (no GApps)', "
        "'GApps'",
    )

    def __str__(self):
        return self.codename
