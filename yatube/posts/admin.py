from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(Post, PostAdmin)


class CDAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'artist')
    list_filter = ('date', 'genre')
    empty_value_display = '-пусто-'
