from datetime import datetime

from django.views.generic import ListView, DetailView
from .models import Post


class PostList(ListView):

    model = Post
    # ordering = 'title'
    queryset = Post.objects.order_by('-post_date')
    template_name = 'posts.html'
    context_object_name = 'posts'


class PostDetail(DetailView):

    model = Post
    template_name = 'post.html'
    context_object_name = 'post'