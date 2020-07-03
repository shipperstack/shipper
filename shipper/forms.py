from django import forms

from .validators import validate_file_extension


class BuildUploadForm(forms.Form):
    build_file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        # validators=[validate_file_extension]
    )
