from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Post(models.Model):
    text = models.TextField(verbose_name='Текст поста')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='posts', verbose_name='Автор')
    group = models.ForeignKey('Group',
                              blank=True,
                              null=True,
                              on_delete=models.SET_NULL,
                              related_name='posts', verbose_name='Сообщество')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-pub_date', 'author']


class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=200, verbose_name='Слаг', unique=True)
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Сообщество'
        verbose_name_plural = 'Сообщества'
        ordering = ['title']
