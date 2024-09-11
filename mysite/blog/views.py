from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Category, Article, Tag
from django.db.models import Q, F
from datetime import datetime
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .forms import AddForm


def index(request):
    article_list = Article.objects.filter(is_draft=False).order_by('-add_date')
    paginator = Paginator(article_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'blog/index.html', context)


def category_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    articles = category.article_set.all()
    paginator = Paginator(articles, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'category': category, 'page_obj': page_obj}
    return render(request, 'blog/list.html', context)


def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    # ordered by article id
    prev_article = Article.objects.filter(id__lt=article_id).last()
    next_article = Article.objects.filter(id__gt=article_id).first()

    print(article.views)
    Article.objects.filter(id=article_id).update(views=F('views') + 1)  # not recommended
    context = {'article': article, 'prev_article': prev_article, 'next_article': next_article}
    return render(request, 'blog/detail.html', context)


def search(request):
    keyword = request.GET.get('keyword')

    if not keyword:
        article_list = Article.objects.all()
    else:
        article_list = Article.objects.filter(Q(title__icontains=keyword) | Q(title__icontains=keyword) | Q(content__icontains=keyword))
    paginator = Paginator(article_list, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'blog/index.html', context)


def archives(request, year, month):
    article_list = Article.objects.filter(add_date__year=year, add_date__month=month)
    paginator = Paginator(article_list, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    month_name = datetime(year=int(year), month=int(month), day=1).strftime('%B')
    context = {'page_obj': page_obj, 'article_list': article_list, 'year': year, 'month': month_name}
    return render(request, 'blog/archives_list.html', context)


@login_required(login_url='users:login')
def add_article(request):
    if request.method == "POST":
        form = AddForm(request.POST, request.FILES)
        if form.is_valid():
            new_article = form.save(commit=False)
            new_article.owner = request.user

            # 判断用户点击了哪个按钮
            if 'publish' in request.POST:
                new_article.is_draft = False
            elif 'save_as_draft' in request.POST:
                new_article.is_draft = True

            # 保存文章实例到数据库
            new_article.save()

            # 处理用户选择的标签
            tags = form.cleaned_data.get('tags')
            if tags:
                # 由于文章已保存，now we can set tags safely
                new_article.tags.set(tags)
                new_article.save()

            # 如果是草稿，则将草稿保存到 session
            if new_article.is_draft:
                request.session['draft_article'] = {
                    'title': new_article.title,
                    'description': new_article.description,
                    'content': new_article.content,
                    'tags': [tag.name for tag in new_article.tags.all()],
                    'category': new_article.category.id
                }
                # 使用 reverse 函数获取 URL
                redirect_url = reverse('blog:draft_list')
            else:
                redirect_url = reverse('blog:index')
            return JsonResponse({'success': True, 'redirect': redirect_url})

        else:
            # Return form errors as JSON
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = AddForm()

    return render(request, 'users/add_article.html', {'add_form': form})


@login_required(login_url='users:login')
def draft_list(request):
    drafts = request.session.get('draft_article', [])
    return render(request, 'blog/draft_list.html', {'drafts': drafts})
