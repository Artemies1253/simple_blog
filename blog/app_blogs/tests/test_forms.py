from django.test import TestCase
from ..forms import BlogForm, PostDownloadForm, PostForm


class BlogFormTest(TestCase):
    def test_fields(self):
        form = BlogForm()
        fields = ["name", "author_info", "nickname"]
        self.assertEqual(list(form.fields.keys()), fields)


class PostFormTest(TestCase):
    def test_fields(self):
        form = PostForm()
        fields = ["name", "content", "image"]
        self.assertEqual(list(form.fields.keys()), fields)

    def test_image_required(self):
        form = PostForm()
        self.assertFalse(form.fields["image"].required)

    def test_image_ClearableFileInput_multiple(self):
        form = PostForm()
        self.assertTrue(form.fields["image"].widget.attrs["multiple"])


class PostDownloadFormTest(TestCase):
    def test_file_label(self):
        form = PostDownloadForm()
        self.assertEqual(form.fields["file"].label, "csv.файл с постами")
