from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.contrib.auth.models import User
from datetime import datetime, timezone


class Author(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    _rating = models.IntegerField(default=0)

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

    def __str__(self):
        return self.name.title()


class Post(models.Model):

    article = 'AR'
    news = 'NE'

    CHOICE_LIST = [
        (news, 'Новости'),
        (article, 'Статья')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, through='PostCategory')
    p_type = models.CharField(max_length=5, choices=CHOICE_LIST, default=news)
    post_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
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


class PostCategory(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


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
