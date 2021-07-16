from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Blog, Post


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["name", "author_info", "nickname"]


class PostForm(forms.ModelForm, ):
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={"multiple": True}))

    class Meta:
        model = Post
        fields = ["name", "content", "image"]


class PostDownloadForm(forms.Form):
    file = forms.FileField(label=_("csv.файл с постами"))
