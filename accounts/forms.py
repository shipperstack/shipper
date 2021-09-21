from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True
            self.fields[field].help_text = "Required."

    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_verify = forms.CharField(label='Verify Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        required = ['email']    # Warning: do not put username as required (already is)

    def clean_password_verify(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password_verify']:
            raise forms.ValidationError('The passwords do not match!')
        return cd['password_verify']

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError('This email address is already registered and cannot be used!')
        return self.cleaned_data['email']
