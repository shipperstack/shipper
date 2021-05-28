from django.test import TestCase

from accounts.forms import RegisterForm


class RegisterFormTestCase(TestCase):
    def test_mismatched_password(self):
        form = RegisterForm(
            data={
                "username": "tester",
                "first_name": "Test",
                "last_name": "Tester",
                "email": "tester@example.com",
                "password": "12345",
                "password_verify": "12842",
                }
        )

        self.assertEqual(form.errors["password_verify"], ["The passwords do not match!"])

    def test_missing_email(self):
        form = RegisterForm(
            data={
                "username": "tester",
                "first_name": "Test",
                "last_name": "Tester",
                "password": "12345",
                "password_verify": "12345",
            }
        )

        self.assertEqual(form.errors["email"], ["This field is required."])

    def test_missing_username(self):
        form = RegisterForm(
            data={
                "first_name": "Test",
                "last_name": "Tester",
                "email": "tester@example.com",
                "password": "12345",
                "password_verify": "12345",
            }
        )

        self.assertEqual(form.errors["username"], ["This field is required."])
