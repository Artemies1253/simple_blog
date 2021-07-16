from django.test import TestCase
from django.urls import reverse
from ..models import Blog, Post, PostImage
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
import os


class BlogListViewTest(TestCase):
    def test_blog_list_status_code(self):
        response = self.client.get(reverse("blog_list"))
        self.assertEqual(response.status_code, 200)

    def test_blog_list_uses_correct_template(self):
        response = self.client.get(reverse("blog_list"))
        self.assertTemplateUsed(response, "blogs/blog_list.html")


class BlogDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username="Dean", password="12345")
        Blog.objects.create(name="test_blog", author=user, author_info="test_author_info", nickname="test_nickname")

    def test_blog_detail_status_code(self):
        response = self.client.get(reverse("blog_detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 200)

    def test_blog_detail_uses_correct_template(self):
        response = self.client.get(reverse("blog_detail", kwargs={"pk": 1}))
        self.assertTemplateUsed("blogs/blog_create.html")


class CreateBlogViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="Dean", first_name="Dean", last_name="Winchester", password="12345")

    def test_create_blog_if_not_logged_in(self):
        response = self.client.get(reverse("blog_create"))
        self.assertRedirects(response, expected_url="/user/login/?next=/blog/create_blog",
                             status_code=302, target_status_code=200)

    def test_create_blog_if_logged_in(self):
        login = self.client.login(username="Dean", password="12345")
        response = self.client.get(reverse("blog_create"))
        self.assertEqual(response.status_code, 200)

    def test_create_blog_uses_correct_template(self):
        login = self.client.login(username="Dean", password="12345")
        response = self.client.get(reverse("blog_create"))
        self.assertTemplateUsed("blogs/blog_create")

    def test_create_blog_no_valid_data(self):
        login = self.client.login(username="Dean", password="12345")
        data = {"author_info": "test_author_info"}
        response = self.client.post(reverse("blog_create"), data)
        self.assertEqual(response.status_code, 200)
        blog = Blog.objects.filter(id=1)
        self.assertFalse(blog)

    def test_create_blog_valid_data(self):
        login = self.client.login(username="Dean", password="12345")
        data = {"name": "test_blog", "author_info": "test_author_info", "nickname": "test_nickname"}
        response = self.client.post(reverse("blog_create"), data)
        self.assertRedirects(response, expected_url="/blog/blog_list/", status_code=302, target_status_code=200)
        blog = Blog.objects.filter(id=1).first()
        self.assertTrue(blog)
        self.assertEqual(blog.name, "test_blog")
        self.assertEqual(blog.author_info, "test_author_info")
        self.assertEqual(blog.nickname, "test_nickname")

    def test_create_blog_valid_data_without_nickname(self):
        login = self.client.login(username="Dean", password="12345")
        data = {"name": "test_blog", "author_info": "test_author_info"}
        response = self.client.post(reverse("blog_create"), data)
        self.assertRedirects(response, expected_url="/blog/blog_list/", status_code=302, target_status_code=200)
        blog = Blog.objects.filter(id=1).first()
        self.assertTrue(blog)
        self.assertEqual(blog.nickname, "Dean Winchester")


class RedactBlogTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="Dean", first_name="Dean", last_name="Winchester", password="12345")
        blog = Blog.objects.create(name="test_blog", author=user,
                                   author_info="test_author_info", nickname="test_nickname")

    def test_redact_blog_if_not_logged_in(self):
        response = self.client.get(reverse("blog_redact", kwargs={"pk": 1}))
        self.assertRedirects(response, expected_url="/user/login/?next=/blog/redact/1",
                             status_code=302, target_status_code=200)

    def test_redact_blog_if_logged_in(self):
        login = self.client.login(username="Dean", password="12345")
        response = self.client.get(reverse("blog_redact", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 200)

    def test_redact_blog_uses_correct_template(self):
        login = self.client.login(username="Dean", password="12345")
        response = self.client.get(reverse("blog_redact", kwargs={"pk": 1}))
        self.assertTemplateUsed(response, "blogs/blog_redact.html")


class CreatePostViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="Dean", first_name="Dean", last_name="Winchester", password="12345")
        blog = Blog.objects.create(name="test_blog", author=user,
                                   author_info="test_author_info", nickname="test_nickname")

    def test_create_post_if_not_logged_in(self):
        response = self.client.get(reverse("create_post", kwargs={"pk": 1}))
        self.assertRedirects(response, expected_url="/user/login/?next=/blog/create_post/1",
                             status_code=302, target_status_code=200)

    def test_create_post_if_logged_in(self):
        login = self.client.login(username="Dean", password="12345")
        response = self.client.get(reverse("create_post", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 200)

    def test_create_post_uses_correct_template(self):
        login = self.client.login(username="Dean", password="12345")
        response = self.client.get(reverse("create_post", kwargs={"pk": 1}))
        self.assertTemplateUsed(response, "blogs/post_create.html")

    def test_create_post_no_valid_data(self):
        login = self.client.login(username="Dean", password="12345")
        no_valid_data = {"name": "test_post"}
        response = self.client.post(reverse("create_post", kwargs={"pk": 1}), no_valid_data)
        self.assertEqual(response.status_code, 200)
        post = Post.objects.filter(id=1, name="test_post").first()
        self.assertFalse(post)

    def test_create_post_valid_data(self):
        login = self.client.login(username="Dean", password="12345")
        data = {"name": "test_post", "content": "test_content"}
        response = self.client.post(reverse("create_post", kwargs={"pk": 1}), data)
        self.assertRedirects(response, expected_url=reverse("blog_detail", kwargs={"pk": 1}),
                             status_code=302, target_status_code=200)
        post = Post.objects.filter(id=1, name="test_post").first()
        self.assertTrue(post)
        self.assertEqual(post.name, "test_post")
        self.assertEqual(post.content, "test_content")

    def test_create_post_with_file(self):
        login = self.client.login(username="Dean", password="12345")
        name_test_file = "test_image_file.jpg"
        path_to_test_image = settings.BASE_DIR + "/test_files/" + name_test_file
        path_to_created_image = settings.MEDIA_ROOT + "/image_posts"
        path_to_created_test_image = f"{path_to_created_image}/{name_test_file}"
        while os.path.exists(path_to_created_test_image):
            os.remove(path_to_created_test_image)
        test_image_file = SimpleUploadedFile(name=name_test_file,
                                             content=open(path_to_test_image, "rb").read(), content_type="image/jpeg")
        data = {"name": "test_post", "content": "test_content", "image": [test_image_file]}
        response = self.client.post(reverse("create_post", kwargs={"pk": 1}), data)
        post = Post.objects.filter(id=1).first()
        self.assertTrue(post)
        post_image = post.post_image.filter(post=post)
        self.assertTrue(post_image)
        self.assertTrue(os.path.exists(path_to_created_test_image))
        os.remove(path_to_created_test_image)

    def test_create_post_with_file(self):
        login = self.client.login(username="Dean", password="12345")
        test_image_files = []
        name_test_file = "test_image_file.jpg"
        path_to_test_image = settings.BASE_DIR + "/test_files/" + name_test_file
        path_to_created_image = settings.MEDIA_ROOT + "/image_posts"
        path_to_created_test_image = f"{path_to_created_image}/{name_test_file}"
        while os.path.exists(path_to_created_test_image):
            os.remove(path_to_created_test_image)
        test_image_file = SimpleUploadedFile(name=name_test_file,
                                             content=open(path_to_test_image, "rb").read(), content_type="image/jpeg")
        test_image_files.append(test_image_file)
        name_test_file_2 = "test_image_file_2.jpg"
        path_to_test_image_2 = settings.BASE_DIR + "/test_files/" + name_test_file_2
        path_to_created_image = settings.MEDIA_ROOT + "/image_posts"
        path_to_created_test_image_2 = f"{path_to_created_image}/{name_test_file_2}"
        while os.path.exists(path_to_created_test_image_2):
            os.remove(path_to_created_test_image_2)
        test_image_file_2 = SimpleUploadedFile(name=name_test_file_2,
                                               content=open(path_to_test_image_2, "rb").read(),
                                               content_type="image/jpeg")
        test_image_files.append(test_image_file_2)
        data = {"name": "test_post", "content": "test_content", "image": test_image_files}
        response = self.client.post(reverse("create_post", kwargs={"pk": 1}), data)
        post = Post.objects.filter(id=1).first()
        self.assertTrue(post)
        post_images = post.post_image.filter(post=post)
        self.assertTrue(post_images)
        self.assertEqual(len(post_images), 2)
        self.assertTrue(os.path.exists(path_to_created_test_image))
        self.assertTrue(os.path.exists(path_to_created_test_image_2))
        os.remove(path_to_created_test_image)
        os.remove(path_to_created_test_image_2)


class PostDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="Dean", first_name="Dean", last_name="Winchester", password="12345")
        blog = Blog.objects.create(name="test_blog", author=user,
                                   author_info="test_author_info", nickname="test_nickname")
        post = Post.objects.create(name="test_post", content="test_content", blog=blog)

    def test_post_detail_status_code(self):
        response = self.client.get(reverse("post_detail", kwargs={"slug": "test_post"}))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_uses_correct_templates(self):
        response = self.client.get(reverse("post_detail", kwargs={"slug": "test_post"}))
        self.assertTemplateUsed(response, "blogs/post_detail.html")


class DownloadPostViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="Dean", first_name="Dean", last_name="Winchester", password="12345")
        blog = Blog.objects.create(name="test_blog", author=user,
                                   author_info="test_author_info", nickname="test_nickname")

    def test_download_post_if_not_logged_in(self):
        response = self.client.post(reverse("post_download", kwargs={"pk": 1}))
        self.assertRedirects(response, expected_url="/user/login/?next=/blog/post_download/1",
                             status_code=302, target_status_code=200)

    def test_dowlnoad_post_if_logged_in(self):
        login = self.client.login(username="Dean", password="12345")
        response = self.client.post(reverse("post_download", kwargs={"pk": 1}))
        self.assertRedirects(response, expected_url=reverse("blog_detail", kwargs={"pk": 1}),
                             status_code=302, target_status_code=200)

    def test_download_post_valid_data(self):
        login = self.client.login(username="Dean", password="12345")
        name_file_test_csv = "test_csv.csv"
        path_file_test_csv = settings.BASE_DIR + "/test_files/" + name_file_test_csv
        test_file_csv = SimpleUploadedFile(name=name_file_test_csv,
                                           content=open(path_file_test_csv, "rb").read(),
                                           content_type="text/csv")
        data = {"file": test_file_csv}
        self.assertEqual(Post.objects.all().count(), 0)
        response = self.client.post(reverse("post_download", kwargs={"pk": 1}), data)
        self.assertEqual(Post.objects.all().count(), 2)


