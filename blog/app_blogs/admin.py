from django.contrib import admin
from .models import Blog, Post
from django.contrib.admin import register


class InlinesPost(admin.TabularInline):
    model = Post


@register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ["name", "author"]
    inlines = [InlinesPost]


@register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["name", "content", "blog"]
