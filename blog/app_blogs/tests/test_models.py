from django.test import TestCase
from ..models import Blog, Post, PostImage
from django.contrib.auth.models import User
from django.conf import settings


class BlogModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username="Dean", password="12345")
        Blog.objects.create(name="test_blog", author=user, author_info="test_author_info", nickname="test_nickname")

    def test_name_label(self):
        blog = Blog.objects.get(id=1)
        field_label = blog._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "Имя блога")

    def test_name_max_length(self):
        blog = Blog.objects.get(id=1)
        max_length = blog._meta.get_field("name").max_length
        self.assertEqual(max_length, 30)

    def test_author_on_delete(self):
        user = User.objects.get(id=1)
        blogs = Blog.objects.filter(author=user)
        self.assertTrue(blogs)
        user.delete()
        blogs = Blog.objects.filter(author=user)
        self.assertFalse(blogs)
        blog = Blog.objects.filter(id=1)
        self.assertFalse(blog)

    def test_author_info_label(self):
        blog = Blog.objects.get(id=1)
        field_label = blog._meta.get_field("author_info").verbose_name
        self.assertEqual(field_label, "Информация о себе")

    def test_author_info_max_length(self):
        blog = Blog.objects.get(id=1)
        max_length = blog._meta.get_field("author_info").max_length
        self.assertEqual(max_length, 200)

    def test_nickname_info_label(self):
        blog = Blog.objects.get(id=1)
        field_label = blog._meta.get_field("nickname").verbose_name
        self.assertEqual(field_label, "Прозвище")

    def test_nickname_info_max_length(self):
        blog = Blog.objects.get(id=1)
        max_length = blog._meta.get_field("nickname").max_length
        self.assertEqual(max_length, 80)


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username="Dean", password="12345")
        blog = Blog.objects.create(name="test_blog", author=user,
                                   author_info="test_author_info", nickname="test_nickname")
        Post.objects.create(name="test_post", content="test_content", blog=blog)

    def test_name_label(self):
        post = Post.objects.get(id=1)
        verbose_name = post._meta.get_field("name").verbose_name
        self.assertEqual(verbose_name, "Заголовок")

    def test_name_max_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field("name").max_length
        self.assertEqual(max_length, 30)

    def test_content_label(self):
        post = Post.objects.get(id=1)
        verbose_name = post._meta.get_field("content").verbose_name
        self.assertEqual(verbose_name, "Текст")

    def test_blog_label(self):
        post = Post.objects.get(id=1)
        verbose_name = post._meta.get_field("blog").verbose_name
        self.assertEqual(verbose_name, "Блог")

    def test_blog_on_delete(self):
        blog = Blog.objects.get(id=1)
        post = Post.objects.filter(blog=blog, name="test_post")
        self.assertTrue(post)
        blog.delete()
        post = Post.objects.filter(blog=blog, name="test_post")
        self.assertFalse(post)

    def test_blog_related_name(self):
        blog = Blog.objects.get(id=1)
        post_related_name = blog.post.all()
        self.assertTrue(post_related_name)

    def test_date_created_label(self):
        post = Post.objects.get(id=1)
        date_created_label = post._meta.get_field("date_created").verbose_name
        self.assertEqual(date_created_label, "Дата создания")

    def test_date_created_auto_now_add(self):
        post = Post.objects.get(id=1)
        date_created_auto_now_add = post._meta.get_field("date_created").auto_now_add
        self.assertTrue(date_created_auto_now_add)

    def test_date_updated_label(self):
        post = Post.objects.get(id=1)
        date_updated_label = post._meta.get_field("date_updated").verbose_name
        self.assertEqual(date_updated_label, "Дата изменения")

    def test_date_updated_auto_now(self):
        post = Post.objects.get(id=1)
        date_created_auto_now = post._meta.get_field("date_updated").auto_now
        self.assertTrue(date_created_auto_now)

    def test_absolute_url(self):
        post = Post.objects.get(id=1)
        expected_url = f"/blog/post_detail/{post.name}"
        self.assertEqual(post.get_absolute_url(), expected_url)

    def test_post_verbose_name(self):
        post = Post.objects.get(id=1)
        verbose_name = post._meta.verbose_name
        self.assertEqual(verbose_name, "Пост")

    def test_post_verbose_name_plural(self):
        post = Post.objects.get(id=1)
        verbose_name_plural = post._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, "Посты")

    def test_post_ordering(self):
        post = Post.objects.get(id=1)
        ordering = post._meta.ordering
        self.assertEqual(ordering, ["date_updated"])


class PostImageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username="Dean", password="12345")
        blog = Blog.objects.create(name="test_blog", author=user,
                                   author_info="test_author_info", nickname="test_nickname")
        post = Post.objects.create(name="test_post", content="test_content", blog=blog)
        path_file = settings.BASE_DIR + "test_image_file.jpg"
        PostImage.objects.create(post=post, image=path_file)

    def test_image_label(self):
        post_image = PostImage.objects.get(id=1)
        verbose_name = post_image._meta.get_field("image").verbose_name
        self.assertEqual(verbose_name, "Изображение")

    def test_post_on_delete(self):
        post = Post.objects.get(id=1)
        post_image = PostImage.objects.filter(id=1)
        self.assertTrue(post_image)
        post.delete()
        post_image = PostImage.objects.filter(id=1)
        self.assertFalse(post_image)

    def test_post_related_name(self):
        post = Post.objects.get(id=1)
        post_images = post.post_image.all()
        self.assertTrue(post_images)
