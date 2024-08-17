from django.db import models
from django.contrib.auth.models import User


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


class Article(models.Model):
    title = models.CharField(max_length=60, verbose_name='Article')
    description = models.TextField(max_length=200, verbose_name='Article Description')
    content = models.TextField(verbose_name='Article Content')
    tags = models.ForeignKey(Tag, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Article Tags')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')
    add_date = models.DateTimeField(auto_now_add=True, verbose_name='Publish Time')
    mod_date = models.DateTimeField(auto_now_add=True, verbose_name='Last Modified Time')

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
