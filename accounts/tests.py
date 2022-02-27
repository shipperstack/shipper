from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase

from .forms import RegisterForm
from .views import register

User = get_user_model()


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_register_view_get(self):
        request = self.factory.get("register/")
        request.user = AnonymousUser()
        response = register(request=request)

        self.assertEqual(response.status_code, 200)


class RegisterFormTestCase(TestCase):
    def setUp(self):
        create_test_user(
            username="tester1",
            first_name="Test",
            last_name="Tester",
            email="tester@example.com",
            password="12345",
        )

    def test_mismatched_password(self):
        form = RegisterForm(
            data={
                "username": "tester2",
                "first_name": "Test",
                "last_name": "Tester",
                "email": "tester2@example.com",
                "password": "12345",
                "password_verify": "12842",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["password_verify"], ["The passwords do not match!"]
        )

    def test_missing_email(self):
        form = RegisterForm(
            data={
                "username": "tester2",
                "first_name": "Test",
                "last_name": "Tester",
                "password": "12345",
                "password_verify": "12345",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["email"], ["This field is required."])

    def test_missing_username(self):
        form = RegisterForm(
            data={
                "first_name": "Test",
                "last_name": "Tester",
                "email": "tester2@example.com",
                "password": "12345",
                "password_verify": "12345",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["username"], ["This field is required."])

    def test_duplicate_email(self):
        form = RegisterForm(
            data={
                "username": "tester2",
                "first_name": "Test",
                "last_name": "Tester",
                "email": "tester@example.com",
                "password": "12345",
                "password_verify": "12345",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["email"],
            ["This email address is already registered and cannot be used!"],
        )


def create_test_user(username, first_name, last_name, email, password):
    User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
    )
