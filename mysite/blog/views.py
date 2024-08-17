from django.shortcuts import render
from .models import Category, Article, Tag
# Create your views here.


def index(request):
    category_list = Category.objects.all()
    article_list = Article.objects.all()
    context = {'category_list': category_list, 'article_list': article_list}
    return render(request, 'blog/index.html', context)
