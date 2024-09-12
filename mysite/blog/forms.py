from django import forms
from django.core.exceptions import ValidationError

from .models import Article, Tag


class AddForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Article
        fields = ('title', 'description', 'content', 'category', 'tags',)  # 不包括 tags 和 owner


class ArticleForm(forms.ModelForm):
    # 处理标签，使用多选字段，并显示为复选框
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),  # 获取所有标签
        widget=forms.CheckboxSelectMultiple,  # 使用复选框来选择多个标签
        required=False  # 标签为非必填项
    )

    class Meta:
        model = Article
        # 定义需要的字段
        fields = ['title', 'description', 'content', 'category', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter the title'}),
            'description': forms.Textarea(attrs={'class': 'textarea', 'placeholder': 'Enter the description'}),
            'content': forms.Textarea(attrs={'class': 'textarea', 'placeholder': 'Enter the content'}),
            'category': forms.Select(attrs={'class': 'select'}),
        }

    # 你可以选择性地添加自定义的验证逻辑
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise ValidationError('Title cannot be empty.')
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        return content
