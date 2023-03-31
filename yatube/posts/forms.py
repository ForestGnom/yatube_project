from django.utils.translation import gettext_lazy as _

from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')

        labels = {
            'text': _('Текст поста'),
            'group': _('Группа'),
        }

        help_texts = {
            'text': _('Текст нового поста'),
            'group': _('Группа, к которой будет относиться пост')
        }

        widgets = {
            'text': forms.Textarea(attrs={'cols': 40, 'rows': 10, 'class': 'form-control', 'id': 'id_text'}),
            'group': forms.Select(attrs={'class': 'form-control', 'id': 'id_group'})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

        widgets = {
            'text': forms.Textarea(attrs={'cols': 40, 'rows': 10, 'class': 'form-control', 'id': 'id_text'}),
        }
