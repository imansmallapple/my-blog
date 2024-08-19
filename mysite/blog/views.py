from django.shortcuts import render, get_object_or_404
from .models import Category, Article, Tag
# Create your views here.


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
    context = {'article': article}
    return render(request, 'blog/detail.html', context)
