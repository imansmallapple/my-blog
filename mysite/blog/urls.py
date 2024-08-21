from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:category_id>', views.category_list, name='category_list'),
    path('article/<int:article_id>', views.article_detail, name='article_detail'),
    path('search/', views.search, name='search'),
    path('archives/<int:year>/<int:month>/', views.archives, name='archives'),
]