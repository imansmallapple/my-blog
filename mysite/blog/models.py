from django.db import models
from django.contrib.auth.models import User
from django.utils.functional import cached_property
from django.template.loader import render_to_string


class Category(models.Model):
    name = models.CharField(max_length=32, verbose_name='Category Name')
    description = models.TextField(max_length=200, blank=True, default='', verbose_name='Category description')
    add_date = models.DateTimeField(auto_now_add=True, verbose_name='Publish Time')
    mod_date = models.DateTimeField(auto_now_add=True, verbose_name='Last Modified Time')

    class Meta:
        verbose_name = 'Blog Category'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=10, verbose_name='Article Tag')
    add_date = models.DateTimeField(auto_now_add=True, verbose_name='Publish Time')
    mod_date = models.DateTimeField(auto_now_add=True, verbose_name='Last Modified Time')

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=60, verbose_name='Article')
    description = models.TextField(max_length=200, verbose_name='Article Description')
    content = models.TextField(verbose_name='Article Content')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='Article Tags')  # 使用 ManyToManyField
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')
    add_date = models.DateTimeField(auto_now_add=True, verbose_name='Publish Time')
    mod_date = models.DateTimeField(auto_now=True, verbose_name='Last Modified Time')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Category')
    is_hot = models.BooleanField(default=False, verbose_name='Is Popular')
    views = models.IntegerField(default=0, verbose_name='Views')
    is_draft = models.BooleanField(default=False, verbose_name='Is Draft')

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', verbose_name='Article')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')  # 评论者
    content = models.TextField(verbose_name='Comment Content')  # 评论内容
    add_date = models.DateTimeField(auto_now_add=True, verbose_name='Created Time')  # 评论创建时间
    mod_date = models.DateTimeField(auto_now=True, verbose_name='Updated Time')  # 评论更新时间
    is_hot = models.BooleanField(default=False, verbose_name='Is Popular')

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-add_date']  # 按时间倒序排列评论

    def __str__(self):
        return f'Comment by {self.user.username} on {self.article.title}'


class SideBar(models.Model):
    STATUS = (
        (1, 'Hide'),
        (2, 'Perform'),
    )

    DISPLAY_TYPE = (
        (1, 'Search'),
        (2, 'Newest Article'),
        (3, 'Hottest Article'),
        (4, 'Recently Comment'),
        (5, 'Article Archiving'),
        (6, 'HTML'),
    )

    title = models.CharField(max_length=50, verbose_name='Title')
    display_type = models.PositiveIntegerField(default=1, choices=DISPLAY_TYPE, verbose_name='Display types')
    content = models.CharField(max_length=500, blank=True, default='', verbose_name='Content',
                               help_text="Can be empty if setting isn't HTML type")
    sort = models.PositiveIntegerField(default=1, verbose_name='Sort', help_text="Larger id with former place")
    status = models.PositiveIntegerField(default=2, choices=STATUS, verbose_name="Status")
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="Created Time")

    class Meta:
        verbose_name = "Side bar"
        verbose_name_plural = verbose_name
        ordering = ['-sort']

    def __str__(self):
        return self.title

    @classmethod
    def get_sidebar(cls):
        return cls.objects.filter(status=2)

    @property
    def get_content(self):
        if self.display_type == 1:
            context = {}
            return render_to_string('blog/sidebar/search.html', context=context)

        elif self.display_type == 2:
            context = {}
            return render_to_string('blog/sidebar/new_article.html', context=context)

        elif self.display_type == 3:
            context = {}
            return render_to_string('blog/sidebar/hot_article.html', context=context)

        elif self.display_type == 4:
            context = {}
            return render_to_string('blog/sidebar/comment.html', context=context)

        elif self.display_type == 5:
            context = {}
            return render_to_string('blog/sidebar/archives.html', context=context)
        elif self.display_type == 6:

            return self.content
