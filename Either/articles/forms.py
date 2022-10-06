from django import forms
from .models import Article, Comment


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        # exclude = ('author',)
        widgets = {
            'img': forms.Textarea(attrs={'style': 'height: 50px;width:250px'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # fields = '__all__'
        exclude = ('article',)
