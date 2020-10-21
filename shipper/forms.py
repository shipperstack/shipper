from django import forms

from .validators import *


class BuildUploadForm(forms.Form):
    zip_file = forms.FileField(validators=[validate_build_file_extension])
    md5_file = forms.FileField(validators=[validate_checksum_file_extension])
