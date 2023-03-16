from django.urls import path
from . import views


app_name = 'posts'


urlpatterns = [
    path('', views.index, name='index'),
    path('groups/<slug:slug>/', views.groups_posts, name='group_list')
]
