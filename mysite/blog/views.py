from django.shortcuts import render, get_object_or_404
from .models import Category, Article, Tag
from django.db.models import Q, F


def index(request):
    category_list = Category.objects.all()
    article_list = Article.objects.all()
    context = {'category_list': category_list, 'article_list': article_list}
    return render(request, 'blog/index.html', context)


def category_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    articles = category.article_set.all()
    context = {'category': category, 'article_list': articles}
    return render(request, 'blog/list.html', context)


def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    # ordered by article id
    prev_article = Article.objects.filter(id__lt=article_id).last()
    next_article = Article.objects.filter(id__gt=article_id).first()

    context = {'article': article, 'prev_article': prev_article, 'next_article': next_article}
    return render(request, 'blog/detail.html', context)


def search(request):
    keyword = request.GET.get('keyword')

    if not keyword:
        article_list = Article.objects.all()
    else:
        article_list = Article.objects.filter(Q(title__icontains=keyword) | Q(title__icontains=keyword) | Q(content__icontains=keyword))
    context = {
        'article_list': article_list
    }
    return render(request, 'blog/index.html', context)
