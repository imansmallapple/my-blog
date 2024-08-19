from django.contrib import admin
from .models import Category, Article, Tag, SideBar

admin.site.register(Category)
admin.site.register(Article)
admin.site.register(Tag)
admin.site.register(SideBar)