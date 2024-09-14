from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:category_id>', views.category_list, name='category_list'),
    path('article/<int:article_id>', views.article_detail, name='article_detail'),
    path('search/', views.search, name='search'),
    path('archives/<int:year>/<int:month>/', views.archives, name='archives'),
    path('add_article/', views.add_article, name='add_article'),
    path('published_articles/', views.published_articles, name='published_articles'),
    path('edit_article/<int:article_id>/', views.edit_article, name='edit_article'),
    path('drafts/', views.draft_list, name='draft_list'),
    path('delete_article/<int:article_id>', views.delete_article, name='delete_article'),
    path('delete_comment/<int:comment_id>', views.delete_comment, name='delete_comment'),
    path('comment_list/', views.comment_list, name='comment_list'),
]
