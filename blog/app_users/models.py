from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(
        max_length=20, blank=True, verbose_name=_("Телефон")
    )
    city = models.CharField(max_length=40, blank=True, verbose_name=_("Город"))

    class Meta:
        verbose_name = _("Профиль")
        verbose_name_plural = _("Профили")
