from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')
        widgets = {
            'text': forms.Textarea(attrs={'cols': 40, 'rows': 10, 'class': 'form-control', 'id': 'id_text'}),
            'group': forms.Select(attrs={'class': 'form-control', 'id': 'id_group'})
        }