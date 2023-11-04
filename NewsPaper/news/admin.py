from django.contrib import admin
from .models import Post, Category
from modeltranslation.admin import TranslationAdmin


def simple_func(modeladmin, request, queryset):

    queryset.update()
    simple_func.short_description = 'имя, отображаемое в админ панели'


class PostForAdmin(admin.ModelAdmin):

    """ list_display — это список или кортеж со всеми полями, которые хотим видеть в таблице с постами """
    list_display = ('id', 'title', 'author', 'post_date', 'p_type')
    list_filter = ('author', 'post_date', 'p_type')
    search_fields = ['title', 'author__user__username']
    # actions = [simple_func]


class CategoryForAdmin(admin.ModelAdmin):

    """ list_display — это список или кортеж со всеми полями, которые хотим видеть в таблице с постами """
    list_display = ('id', 'name')
    list_filter = ['name']
    search_fields = ['name']


class CategoryAdmin(TranslationAdmin):
    model = Category


class PostAdmin(TranslationAdmin):
    model = Post


admin.site.register(Post, PostForAdmin)
admin.site.register(Category, CategoryForAdmin)
