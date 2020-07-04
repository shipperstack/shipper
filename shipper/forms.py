from django import forms

from .validators import validate_file_extension
from .models import Build


class BuildUploadForm(forms.Form):
    build_file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        validators=[validate_file_extension]
    )
    gapps = forms.BooleanField()
    release = forms.ChoiceField(choices=Build.RELEASE_CHOICES)
