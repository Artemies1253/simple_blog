from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Profile


class LoginViewTest(TestCase):
    def test_login_status_code(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_login_uses_correct_template(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")


class LogoutViewTest(TestCase):
    def test_logout_exist_at_desired_location(self):
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/logout.html")


class RegistrationViewTest(TestCase):
    def test_registration_exist_at_desired_location(self):
        response = self.client.get(reverse("registration"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/registration.html")

    def setUp(self):
        self.data = {"username": "test_username", "password1": "test_password",
                     "password2": "test_password", "first_name": "test_first_name",
                     "last_name": "test_last_name", "phone": "test_phone", "city": "test_city"}

    def test_registration_user_valid_data(self):
        response = self.client.post(reverse("registration"), self.data)
        self.assertRedirects(response, expected_url="/",
                             status_code=302, target_status_code=200)
        user = User.objects.get(username="test_username", first_name="test_first_name",
                                last_name="test_last_name", )
        self.assertTrue(user)
        profile = Profile.objects.get(user=user, phone="test_phone", city="test_city")
        self.assertTrue(profile)

    def test_registration_user_no_valid_data(self):
        self.data["password1"] = "password"
        response = self.client.post(reverse("registration"), self.data)
        self.assertEqual(response.status_code, 200)
        user = User.objects.filter(username="test_username", first_name="test_first_name",
                                   last_name="test_last_name")
        self.assertFalse(user)


class ProfileViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(username="test_user_1", password="12345",
                                             first_name="Dean", last_name="Winchester")
        profile = Profile.objects.create(user=test_user, phone="127-15-48", city="Dallas")

    def test_profile_status_code_if_not_logged_in(self):
        response = self.client.get(reverse("profile"))
        self.assertRedirects(response, expected_url="/user/login/?next=/user/accounts/profile/",
                             status_code=302, target_status_code=200)

    def test_profile_status_code_if_logged_in(self):
        login = self.client.login(username="test_user_1", password="12345")
        response = self.client.get(reverse("profile"))
        self.assertEqual(str(response.context["user"]), "test_user_1")
        self.assertEqual(response.status_code, 200)

    def test_profile_uses_correct_template(self):
        login = self.client.login(username="test_user_1", password="12345")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile.html")


class ProfileRedactViewTest(TestCase):
    def setUp(self):
        self.data = {"first_name": "Sam", "last_name": "Wi",
                     "phone": "8-800-555-35-35", "city": "Aurora"}
        test_user = User.objects.create_user(username="test_user_1", password="12345",
                                             first_name="Dean", last_name="Winchester")
        profile = Profile.objects.create(user=test_user, phone="127-15-48", city="Dallas")

    def test_profile_redact_status_code_if_not_logged_in_get(self):
        response = self.client.get(reverse("profile_redact"))
        self.assertRedirects(response, expected_url="/user/login/?next=/user/accounts/profile/redact",
                             status_code=302, target_status_code=200)

    def test_profile_redact_uses_correct_template_get(self):
        login = self.client.login(username="test_user_1", password="12345")
        response = self.client.get(reverse("profile_redact"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile_redact.html")

    def test_profile_redact_autocomplete_form_get(self):
        login = self.client.login(username="test_user_1", password="12345")
        response = self.client.get(reverse("profile_redact"))
        self.assertEqual(response.context["profile_form"]["first_name"].value(), "Dean")
        self.assertEqual(response.context["profile_form"]["last_name"].value(), "Winchester")
        self.assertEqual(response.context["profile_form"]["phone"].value(), "127-15-48")
        self.assertEqual(response.context["profile_form"]["city"].value(), "Dallas")

    def test_profile_redact_status_code_post(self):
        login = self.client.login(username="test_user_1", password="12345")
        response = self.client.post(reverse("profile_redact"), self.data)
        self.assertEqual(response.status_code, 302)

    def test_profile_redact_no_valid_form_post(self):
        self.data["first_name"] = "test" * 10
        login = self.client.login(username="test_user_1", password="12345")
        user = User.objects.get(username="test_user_1")
        response = self.client.post(reverse("profile_redact"), self.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.first_name, "Dean")

    def test_profile_redact_valid_form_post(self):
        login = self.client.login(username="test_user_1", password="12345")
        response = self.client.post(reverse("profile_redact"), self.data)
        user = User.objects.get(username="test_user_1")
        self.assertRedirects(response, expected_url="/user/accounts/profile/", status_code=302, target_status_code=200)
        self.assertEqual(user.first_name, "Sam")
        self.assertEqual(user.last_name, "Wi")
        self.assertEqual(user.profile.phone, "8-800-555-35-35")
        self.assertEqual(user.profile.city, "Aurora")
