from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from .forms import PostForm
from .models import *


NUM_OF_PAGES = 10
NUM_OF_SUMBOLS = 30


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, NUM_OF_PAGES)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def groups_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)

    post_list = group.posts.order_by('-pub_date')

    paginator = Paginator(post_list, NUM_OF_PAGES)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'group': group,
        'page_obj': page_obj
    }

    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)

    post_list = Post.objects.filter(author=author)
    count_posts = Post.objects.filter(author=author).count()
    paginator = Paginator(post_list, NUM_OF_PAGES)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'username': username,
        'author': author,
        'count_posts': count_posts,
        'page_obj': page_obj,
    }

    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    title = post.text[:NUM_OF_SUMBOLS]
    count_posts = Post.objects.filter(author=post.author).count()

    context = {
        'post': post,
        'title': title,
        'count_post': count_posts,
    }

    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', username=post.author)
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    is_edit = True
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return redirect('posts:post_detail', post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:post_detail', post_id)
        else:
            context = {'form': form}
            return render(request, 'posts/create_post.html', context)
    else:
        form = PostForm(instance=post)

    context = {'form': form,
               'is_edit': is_edit,
               'post_id': post_id}
    return render(request, 'posts/create_post.html', context)

    # post = get_object_or_404(Post, id=post_id)
    # if request.method == 'GET':
    #     if request.user is not post.author:
    #         return redirect('posts:post_detail', post_id=post.id)
    #     form = PostForm(instance=post)
    #
    # if request.method == 'POST':
    #     form = PostForm(request.POST, instance=post)
    #     if form.is_valid():
    #         form.save()
    #     return redirect('posts:post_detail', post_id=post.id)
