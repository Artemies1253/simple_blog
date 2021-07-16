from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Profile


class ProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username="Dean", password="12345")
        Profile.objects.create(user=user, city="Dallas", phone="127-03-14")

    def test_city_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field("city").verbose_name
        self.assertEqual(field_label, "Город")

    def test_city_max_length(self):
        profile = Profile.objects.get(id=1)
        max_length = profile._meta.get_field("city").max_length
        self.assertEqual(max_length, 40)

    def test_phone_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field("phone").verbose_name
        self.assertEqual(field_label, "Телефон")

    def test_phone_max_length(self):
        profile = Profile.objects.get(id=1)
        max_length = profile._meta.get_field("phone").max_length
        self.assertEqual(max_length, 20)

    def test_profile_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.verbose_name
        self.assertEqual(field_label, "Профиль")

    def test_profile_label_plural(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.verbose_name_plural
        self.assertEqual(field_label, "Профили")
