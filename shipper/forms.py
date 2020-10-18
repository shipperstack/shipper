from django import forms

from .validators import *
from .models import Build


class BuildUploadForm(forms.Form):
    build_file = forms.FileField(validators=[validate_build_file_extension])
    checksum_file = forms.FileField(validators=[validate_checksum_file_extension])
