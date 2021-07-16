from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Blog(models.Model):
    name = models.CharField(max_length=30, verbose_name=_("Имя блога"))
    date_created = models.DateField(auto_now_add=True, verbose_name=_("Дата создания"))
    date_updated = models.DateField(auto_now_add=True, verbose_name=_("Дата последнего поста"))
    author = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="blog", verbose_name=_("Автор"))
    author_info = models.CharField(max_length=200, verbose_name=_("Информация о себе"))
    nickname = models.CharField(max_length=80, blank=True, verbose_name=_("Прозвище"))

    class Meta:
        verbose_name = _("Блог")
        verbose_name_plural = _("Блоги")
        ordering = ["date_created"]

    def __str__(self):
        return self.name


class Post(models.Model):
    name = models.CharField(max_length=30, verbose_name=_("Заголовок"))
    content = models.TextField(verbose_name=_("Текст"))
    date_created = models.DateField(auto_now_add=True, verbose_name=_("Дата создания"))
    date_updated = models.DateField(auto_now=True, verbose_name=_("Дата изменения"))
    blog = models.ForeignKey(to=Blog, on_delete=models.CASCADE, related_name="post", verbose_name=_("Блог"))

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={"slug": self.name})

    class Meta:
        verbose_name = _("Пост")
        verbose_name_plural = _("Посты")
        ordering = ["date_updated"]


class PostImage(models.Model):
    image = models.ImageField(upload_to="image_posts", blank=True, verbose_name=_("Изображение"))
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name="post_image")
