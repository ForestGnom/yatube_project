from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'posts/index.html')


def groups_posts(request, slug):
    return HttpResponse(f'Страница с группами {slug}')
