from django.contrib import admin
from .models import Category, Article, Tag, SideBar

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(SideBar)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'tags', 'owner', 'views', 'is_hot', 'mod_date', )
    list_filter = ('owner', )
    search_fields = ('title', 'description')
    list_editable = ('is_hot', )
    list_display_links = ('title', )

    class Media:
        css = {
            'all': ('ckeditor5/cked.css', )
        }
        js = (
            "https://cdn.bootcdn.net/ajax/libs/jquery/3.7.1/jquery.js",
            "ckeditor5/ckeditor.js",
            "ckeditor5/config.js",
            "ckeditor5/translations/zh.js",
        )


admin.site.register(Article, ArticleAdmin)
