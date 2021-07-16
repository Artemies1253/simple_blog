from django.urls import path
from .views import BlogListView, BlogDetailView, \
    CreateBlogView, RedactBlogView, CreatePostView, PostDetail, DownloadPostView

urlpatterns = [
    path("blog_list/", BlogListView.as_view(), name="blog_list"),
    path("<int:pk>", BlogDetailView.as_view(), name="blog_detail"),
    path("create_blog", CreateBlogView.as_view(), name="blog_create"),
    path("redact/<int:pk>", RedactBlogView.as_view(), name="blog_redact"),
    path("create_post/<int:pk>", CreatePostView.as_view(), name="create_post"),
    path("post_detail/<str:slug>", PostDetail.as_view(), name="post_detail"),
    path('post_download/<int:pk>', DownloadPostView.as_view(), name="post_download")
]
