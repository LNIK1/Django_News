from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from datetime import datetime


class PostList(ListView):

    model = Post
    queryset = Post.objects.order_by('-post_date')
    template_name = 'posts.html'
    context_object_name = 'posts'


class PostDetail(DetailView):

    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(CreateView):

    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    success_url = reverse_lazy('posts')

    def form_valid(self, form):
        post = form.save(commit=False)

        if 'news/create' in self.request.path:
            post.p_type = 'NE'
        elif 'articles/create' in self.request.path:
            post.p_type = 'AR'

        return super().form_valid(form)


class PostUpdate(UpdateView):

    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('posts')

    def form_valid(self, form):

        post = form.save(commit=False)

        if 'news/' in self.request.path and '/update' in self.request.path and post.p_type == 'AR':
            return HttpResponseRedirect('/posts/wrong_type_update/')

        elif 'articles/' in self.request.path and '/update' in self.request.path and post.p_type == 'NE':
            return HttpResponseRedirect('/posts/wrong_type_update/')

        return super().form_valid(form)


class PostDelete(DeleteView):

    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts')


class NewsList(ListView):

    model = Post
    queryset = Post.objects.filter(p_type='NE').order_by('-post_date')
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10


class NewsSearch(ListView):

    model = Post
    queryset = Post.objects.filter(p_type='NE').order_by('-post_date')
    template_name = 'news_search.html'
    context_object_name = 'news'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)

        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # вернет словарь
        context['filterset'] = self.filterset

        return context


class ArticlesList(ListView):

    model = Post
    queryset = Post.objects.filter(p_type='AR').order_by('-post_date')
    template_name = 'articles.html'
    context_object_name = 'articles'
    paginate_by = 10


class WrongTypeUpdateException(ListView):

    model = Post
    template_name = 'wrong_type_edit.html'
