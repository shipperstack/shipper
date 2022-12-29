from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy

User = get_user_model()


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True
            self.fields[field].help_text = gettext_lazy("Required.")

    password = forms.CharField(
        label=gettext_lazy("Password"), widget=forms.PasswordInput
    )
    password_verify = forms.CharField(
        label=gettext_lazy("Verify Password"), widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
        required = ["email"]  # Warning: do not put username as required (already is)

    def clean_password_verify(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password_verify"]:
            raise forms.ValidationError(gettext_lazy("The passwords do not match!"))
        return cd["password_verify"]

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data["email"]).exists():
            raise forms.ValidationError(
                gettext_lazy(
                    "This email address is already registered and cannot be used!"
                )
            )
        return self.cleaned_data["email"]


class EditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True
            self.fields[field].help_text = gettext_lazy("Required.")

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "profile_picture",
                  "bio", "contact_url"]
        required = ["email"]  # Warning: do not put username as required (already is)
