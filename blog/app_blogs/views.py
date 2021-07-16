from django.shortcuts import render
from django import views
from .models import Blog, Post, PostImage
from .forms import BlogForm, PostForm, PostDownloadForm
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from csv import reader


class BlogListView(views.generic.ListView):
    model = Blog
    template_name = "blogs/blog_list.html"
    context_object_name = "blogs"


class BlogDetailView(views.View):
    def get(self, request, pk):
        blog = Blog.objects.get(id=pk)
        form_download = PostDownloadForm()
        return render(request, "blogs/blog_detail.html", {"blog": blog,
                                                          "form_download": form_download})


class CreateBlogView(LoginRequiredMixin, views.generic.CreateView):
    form_class = BlogForm
    context_object_name = "blog_form"
    template_name = "blogs/blog_create.html"

    def post(self, request):
        blog_form = BlogForm(request.POST)
        if blog_form.is_valid():
            new_blog = Blog(**blog_form.cleaned_data)
            author = request.user
            new_blog.author = author
            if not blog_form.cleaned_data["nickname"]:
                nickname = f"{author.first_name} {author.last_name}"
                new_blog.nickname = nickname
            new_blog.save()
            return redirect("blog_list")
        return render(request, "blogs/blog_create.html", {"blog_form": blog_form})


class RedactBlogView(LoginRequiredMixin, views.generic.UpdateView):
    form_class = BlogForm
    model = Blog
    template_name = "blogs/blog_redact.html"
    success_url = "blog_detail"


class CreatePostView(LoginRequiredMixin, views.generic.CreateView):
    form_class = PostForm
    template_name = "blogs/post_create.html"

    def post(self, request, pk):
        form = PostForm(request.POST, request.FILES)
        blog = Blog.objects.get(id=pk)
        if form.is_valid():
            post = Post()
            post.name = form.cleaned_data["name"]
            post.content = form.cleaned_data["content"]
            post.blog = blog
            post.save()
            files = request.FILES.getlist('image')
            if files:
                for file in files:
                    image = PostImage(image=file, post=post)
                    image.save()
            return redirect("blog_detail", pk=pk)
        return render(request, "blogs/post_create.html", {"form": form})


class PostDetail(views.generic.DetailView):
    model = Post
    template_name = "blogs/post_detail.html"
    context_object_name = "post"
    slug_field = "name"


class DownloadPostView(LoginRequiredMixin, views.View):
    def post(self, request, pk):
        post_download_form = PostDownloadForm(request.POST, request.FILES)
        if post_download_form.is_valid():
            file_posts = post_download_form.cleaned_data["file"].read()
            str_posts = file_posts.decode("cp1251").split("\n")
            csv_reader = reader(str_posts, delimiter=";")
            for row in csv_reader:
                if row:
                    Post.objects.create(blog_id=pk, name=row[0], content=row[1])
            return redirect("blog_detail", pk=pk)
        return redirect("blog_detail", pk=pk)
