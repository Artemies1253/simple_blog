from ..forms import RegistrationForm, ProfileForm
from django.test import TestCase


class RegistrationFormTest(TestCase):
    def test_first_name_label(self):
        form = RegistrationForm()
        self.assertEqual(form.fields["first_name"].label, "Имя")

    def test_first_name_max_length(self):
        form = RegistrationForm()
        self.assertEqual(form.fields["first_name"].max_length, 20)

    def test_last_name_label(self):
        form = RegistrationForm()
        self.assertEqual(form.fields["last_name"].label, "Фамилия")

    def test_last_name_length(self):
        form = RegistrationForm()
        self.assertEqual(form.fields["last_name"].max_length, 20)

    def test_phone_label(self):
        form = RegistrationForm()
        self.assertEqual(form.fields["phone"].label, "Телефон")

    def test_phone_max_length(self):
        form = RegistrationForm()
        self.assertEqual(form.fields["phone"].max_length, 20)

    def test_city_label(self):
        form = RegistrationForm()
        self.assertEqual(form.fields["city"].label, "Город")

    def test_city_max_length(self):
        form = RegistrationForm()
        self.assertEqual(form.fields["city"].max_length, 40)

    def test_fields(self):
        form = RegistrationForm()
        fields = ["username", "password1", "password2",
                  "first_name", "last_name", "phone", "city"]
        self.assertEqual(list(form.fields.keys()), fields)


class ProfileFormTest(TestCase):
    def test_first_name_label(self):
        form = ProfileForm()
        self.assertEqual(form.fields["first_name"].label, "Имя")

    def test_first_name_max_length(self):
        form = ProfileForm()
        self.assertEqual(form.fields["first_name"].max_length, 20)

    def test_last_name_label(self):
        form = ProfileForm()
        self.assertEqual(form.fields["last_name"].label, "Фамилия")

    def test_last_name_length(self):
        form = ProfileForm()
        self.assertEqual(form.fields["last_name"].max_length, 20)

    def test_fields(self):
        form = ProfileForm()
        fields = ["first_name", "last_name", "phone", "city"]
        self.assertEqual(list(form.fields.keys()), fields)
