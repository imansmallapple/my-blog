from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Article, Tag, SideBar, Comment

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(SideBar)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'is_draft', 'owner', 'views', 'is_hot', 'mod_date', 'add_date')
    list_filter = ('owner', )
    search_fields = ('title', 'description')
    list_editable = ('is_hot', )
    list_display_links = ('title', )

    # 自定义方法，获取并显示文章的所有标签
    def tags(self, obj):
        return ', '.join([tag.name for tag in obj.tags.all()])  # 拼接所有标签的名字

    tags.short_description = 'Tags'  # 设置列表显示时的列名

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


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'formatted_content', 'article', 'user', 'is_hot', 'likes', 'dislikes', 'mod_date', 'add_date')
    list_filter = ('user', )
    search_fields = ('article__title', 'user__username')
    list_editable = ('is_hot', )
    list_display_links = ('formatted_content', )

    # 使用 format_html 来渲染 content 字段中的 HTML
    def formatted_content(self, obj):
        return format_html(obj.content)  # 这里确保内容是作为 HTML 而不是纯文本显示
    formatted_content.short_description = 'Content'

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
admin.site.register(Comment, CommentAdmin)
