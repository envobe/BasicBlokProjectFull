from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text')
        labels = {
            'text': '正文',
            'title': '标题',
        }
        widgets = {
            'text': forms.Textarea(attrs={'rows': 15}),
        }