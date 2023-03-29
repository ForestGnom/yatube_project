from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from .forms import PostForm
from .models import Group, Post, User
from .utils import page


def index(request):

    post_list = Post.objects.select_related()

    context = {
        'page_obj': page(request, post_list),
    }
    return render(request, 'posts/index.html', context)


def groups_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)

    post_list = group.posts.all()

    context = {
        'group': group,
        'page_obj': page(request, post_list)
    }

    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)

    post_list = author.posts.all()
    count_posts = post_list.count()

    context = {
        'username': username,
        'author': author,
        'count_posts': count_posts,
        'page_obj': page(request, post_list),
    }

    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    count_posts = post.author.posts.count()

    context = {
        'post': post,
        'count_post': count_posts,
    }

    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(
        request.POST or None,
        files=request.FILES or None
    )
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=post.author)
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post_id)

    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    context = {
        'post': post,
        'form': form,
        'is_edit': True,
    }
    return render(request, 'posts/create_post.html', context)


