from django.urls import path
from . import views


app_name = 'posts'


urlpatterns = [
    path('', views.index, name='index'),
    path('groups/', views.groups_posts, name='groups')
]
