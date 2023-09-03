from django import forms
from django_filters import FilterSet, DateFilter, CharFilter

from .models import Post, Author


class PostFilter(FilterSet):

    title = CharFilter(
        field_name='title',
        label='Заголовок',
        lookup_expr='icontains'
    )

    author = CharFilter(
        field_name='author__user__username',
        label='Имя автора',
        lookup_expr='icontains'
    )

    post_date = DateFilter(
        'post_date__date',
        label='Дата публикации',
        widget=forms.DateInput(attrs={'type': 'date'}),
        lookup_expr='gt'
    )

    class Meta:

        model = Post
        fields = ['title', 'author', 'post_date']
