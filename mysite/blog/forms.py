from django import forms
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
