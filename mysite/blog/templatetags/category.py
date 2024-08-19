from django import template
from ..models import Category, SideBar

register = template.Library()


@register.simple_tag
def get_category_list():
    return Category.objects.all()

@register.simple_tag
def get_sidebar_list():
    return SideBar.get_sidebar()

