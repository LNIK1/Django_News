from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.contrib.auth.models import User
from django.core.cache import cache
from datetime import datetime, timezone


class Author(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    _rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username}'

    @property
    def rating(self):
        return self._rating

    def update_rating(self):
        posts_rating = Post.objects.filter(author=self).aggregate(p_rating=Coalesce(Sum("_rating"), 0))['p_rating']
        comm_rating = Comment.objects.filter(user=self.user).aggregate(c_rating=Coalesce(Sum("_rating"), 0))['c_rating']
        posts_comm_rating = Comment.objects.filter(post__author=self).aggregate(pc_rating=Coalesce(Sum("_rating"), 0))['pc_rating']

        self._rating = posts_rating * 3 + comm_rating + posts_comm_rating
        print(f'Рейтинг автора: {self._rating}')
        self.save()


class Category(models.Model):

    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through='SubscribersCategory')

    def __str__(self):
        return self.name.title()


class Post(models.Model):

    article = 'AR'
    news = 'NE'

    CHOICE_LIST = [
        (news, 'Новости'),
        (article, 'Статья')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    categories = models.ManyToManyField(Category, through='PostCategory', verbose_name='Категория')
    p_type = models.CharField(max_length=5, choices=CHOICE_LIST, default=news, verbose_name='Вид')
    post_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.CharField(max_length=255, verbose_name='Содержание')
    _rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.author.user.username} - "{self.title.title()}"'

    @property
    def rating(self):
        return self._rating

    def like(self):
        self._rating += 1
        self.save()

    def dislike(self):
        self._rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[0:124]}...'

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)
        cache.delete(f'post - {self.pk}')


class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    com_date = models.DateTimeField(auto_now_add=True)
    _rating = models.IntegerField(default=0)

    @property
    def rating(self):
        return self._rating

    def like(self):
        self._rating += 1
        self.save()

    def dislike(self):
        self._rating -= 1
        self.save()


class PostCategory(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class SubscribersCategory(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
