from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

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
