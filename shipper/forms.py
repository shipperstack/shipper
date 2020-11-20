from django import forms
from django.core.validators import FileExtensionValidator


class BuildUploadForm(forms.Form):
    zip_file = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['zip'])], label="Build ZIP file")
    md5_file = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['md5'])], label="MD5 file")
