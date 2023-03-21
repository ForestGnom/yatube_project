from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import *

NUM_OF_PAGES = 10


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
