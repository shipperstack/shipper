from django.contrib.auth.models import User
from django import forms


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_verify = forms.CharField(label='Verify Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_password_verify(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password_verify']:
            raise forms.ValidationError('The passwords do not match!')
        return cd['password_verify']