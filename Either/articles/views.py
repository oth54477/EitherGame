from .models import Article, Comment
from .forms import ArticleForm, CommentForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import (
    require_http_methods,
    require_POST,
    require_safe,
)
import random as lib_random

# Create your views here.
@require_safe
def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm()
    # print(form.errors)
    context = {
        'form': form,
    }
    return render(request, 'articles/create.html', context)


@require_safe
def detail(request, pk):
    article = Article.objects.get(pk=pk)
    comment_form = CommentForm()
    comments = article.comment_set.all()
    total = comments.count()
    blue_team = comments.filter(team=True).count()
    red_team = comments.filter(team=False).count()
    if total != 0:
        blue_rate = round((blue_team / total) * 100, 1)
        red_rate = round((red_team / total) * 100, 1)
    else:
        blue_rate = 0
        red_rate = 0
    context = {
        'article': article,
        'comment_form': comment_form,
        'comments': comments,
        'total': total,
        'blue_team': blue_team,
        'red_team': red_team,
        'blue_rate': blue_rate,
        'red_rate': red_rate,
    }
    return render(request, 'articles/detail.html', context)


@require_POST
def delete(request, pk):
    if request.user.is_authenticated:
        article = Article.objects.get(pk=pk)
        article.delete()
    return redirect('articles:index')


@login_required
@require_http_methods(['GET', 'POST'])
def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm(instance=article)
    context = {
        'article': article,
        'form': form,
    }
    return render(request, 'articles/update.html', context)


def comments_create(request, pk):
    article = Article.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.article = article
        comment.save()
    return redirect('articles:detail', article.pk)


def comments_delete(request, article_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect('articles:detail', article_pk)


def random(request):
    articles = Article.objects.all()
    id_arr = [article.pk for article in articles]
    pk = lib_random.choice(id_arr)
    return redirect('articles:detail', pk)
