from django.db import models


class X86Type(models.Model):
    codename = models.TextField(
        max_length=10, help_text="Codename of the x86 type<br>Example: 'GO', 'Bass'"
    )
    description = models.TextField(
        max_length=30,
        help_text="Description of the x86 text, as seen by users<br> Example: 'GO "
        "builds', 'Bass builds'",
    )
