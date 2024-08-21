from django import template
from ..models import Category, SideBar, Article

register = template.Library()


@register.simple_tag
def get_category_list():
    return Category.objects.all()


@register.simple_tag
def get_sidebar_list():
    return SideBar.get_sidebar()


@register.simple_tag
def get_newest_article():
    return Article.objects.order_by('-mod_date')[:3]


@register.simple_tag
def get_hot_article():
    return Article.objects.filter(is_hot=True)[:3]


@register.simple_tag
def get_top_viewed_article():
    return Article.objects.order_by('-views')[:3]


@register.simple_tag
def get_archives():
    return Article.objects.dates('add_date', 'month', order='DESC')[:8]
