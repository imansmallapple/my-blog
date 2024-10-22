from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Category, Article, Tag, Comment
from django.db.models import Q, F
from datetime import datetime
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .forms import AddForm, ArticleForm, CommentForm


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

    # 获取顶级评论并预取每个评论的回复
    comments = article.comments.filter(parent__isnull=True).prefetch_related('replies').order_by('add_date')

    # ordered by article id
    prev_article = Article.objects.filter(id__lt=article_id).last()
    next_article = Article.objects.filter(id__gt=article_id).first()

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.article = article
                comment.user = request.user
                # 检查是否为回复
                parent_id = request.POST.get('parent_id')
                if parent_id:
                    parent_comment = Comment.objects.get(id=parent_id)
                    comment.parent = parent_comment
                comment.save()
                return redirect('blog:article_detail', article_id=article.id)
        else:
            messages.info(request, "Please log in to comment.")
            return redirect(request.path)  # 假设你的登录视图的 URL 名为 'login'
    else:
        form = CommentForm()

    # print(article.views)
    Article.objects.filter(id=article_id).update(views=F('views') + 1)  # not recommended
    context = {
               'article': article,
               'prev_article': prev_article,
               'next_article': next_article,
               'comments': comments,
               'form': form,
               }
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
            # print(request.POST)

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
def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id, owner=request.user)

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()  # Save the updated article
            return JsonResponse({'success': True, 'redirect': reverse('blog:index')})
        else:
            return JsonResponse({'success': False, 'errors': form.errors.as_json()})  # Provide detailed error messages
    else:
        form = ArticleForm(instance=article)

    context = {'add_form': form, 'article': article}
    return render(request, 'users/edit_article.html', context)


@login_required(login_url='users:login')
def published_articles(request):
    user = User.objects.get(id=request.user.id)
    article_list = Article.objects.filter(owner=user, is_draft=False).order_by('-add_date')
    paginator = Paginator(article_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'users/published_articles.html', context)


@login_required(login_url='users:login')
def draft_list(request):
    user = User.objects.get(id=request.user.id)
    drafts = Article.objects.filter(owner=user, is_draft=True).order_by('-add_date')
    paginator = Paginator(drafts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'users/draft_list.html', context)


@login_required(login_url='users:login')
def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id, owner=request.user)
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Chosen article was deleted successfully.')
        return redirect('blog:draft_list')  # 删除成功后重定向到草稿列表页面
    context = {'article': article}
    return render(request, 'users/delete_article.html', context)


@login_required(login_url='users:login')
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Chosen comment was deleted successfully.')
        return redirect('blog:comment_list')  # 删除成功后重定向到草稿列表页面
    context = {'comment': comment}
    return render(request, 'users/delete_comment.html', context)


@login_required(login_url='users:login')
def comment_list(request):
    comments = Comment.objects.filter(user=request.user)
    # if request.method == 'POST':
    #     comment.delete()
    #     messages.success(request, 'Chosen comment was deleted successfully.')
    #     return redirect('blog:comment_list')  # 删除成功后重定向到草稿列表页面
    paginator = Paginator(comments, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'users/comment_list.html', context)


@login_required(login_url='users:login')
def get_comment_replies(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    replies = comment.replies.all()  # 获取所有回复
    reply_data = []

    # 构造回复数据
    for reply in replies:
        reply_data.append({
            'user': reply.user.username,
            'content': reply.content,
            'add_date': reply.add_date.strftime('%Y-%m-%d %H:%M'),
        })

    return JsonResponse({'replies': reply_data})

