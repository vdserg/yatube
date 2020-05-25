from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PostForm
from .models import Post, Group, User


def index(request):
    post_list = Post.objects.order_by("-pub_date").all()
    paginator = Paginator(post_list, 10)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "posts/index.html",
                  {"page": page, "paginator": paginator})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.group_posts.all().order_by("-pub_date")
    paginator = Paginator(post_list, 10)

    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "group.html", {"group": group, "page": page,
                                          "paginator": paginator})


@login_required
def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("posts:index")
    form = PostForm()
    return render(request, "posts/new_post.html", {"form": form,
                                                   "action": "Опубликовать"})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    author_posts = author.author_posts.order_by("-pub_date")
    paginator = Paginator(author_posts, 10)

    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "posts/profile.html", {"author": author,
                                                  "page": page,
                                                  "paginator": paginator})


def post_view(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id)
    post_count = author.author_posts.count()
    return render(request, "posts/post.html", {"author": author,
                                               "post": post,
                                               "post_count": post_count})


@login_required
def post_edit(request, username, post_id):
    user = get_object_or_404(User, username=username)
    if request.user != user:
        return redirect("posts:post", username=username, post_id=post_id)
    post = Post.objects.get(id=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save(commit=False)
            form.author = user
            form.save()
            return redirect("posts:post", username=username, post_id=post.id)
    form = PostForm(initial={"text": post.text, "group": post.group})
    return render(request, "posts/new_post.html", {"form": form,
                                                   "post": post,
                                                   "author": username,
                                                   "action": "Редактировать"})
