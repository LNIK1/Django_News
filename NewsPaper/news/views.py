import os
import pytz

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.translation import gettext
from django.views.decorators.cache import cache_page  # @cache_page(30)
from django.core.cache import cache

from .models import Post, Category, SubscribersCategory
from .filters import PostFilter
from .forms import PostForm
from .tasks import send_email_post_created


class PostList(ListView):

    model = Post
    queryset = Post.objects.order_by('-post_date')
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 15

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_time'] = timezone.now()
        context['timezones'] = pytz.common_timezones

        return context


class PostDetail(DetailView):

    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):

        obj = cache.get(f'post - {self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post - {self.kwargs["pk"]}', obj)

        return obj


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    permission_required = (
        'news.add_post'
    )

    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    success_url = reverse_lazy('posts')

    def form_valid(self, form):
        post = form.save(commit=False)

        if not self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/login/')

        today = timezone.now()
        quantity = Post.objects.filter(author=post.author, post_date__day=today.day).count()

        if quantity >= 3:
            return render(self.request, 'posts_day_limit.html')

        if 'news/create' in self.request.path:
            post.p_type = 'NE'
        elif 'articles/create' in self.request.path:
            post.p_type = 'AR'

        post.save()
        send_email_post_created.delay(post.id)

        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    permission_required = (
        'news.change_post'
    )

    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('posts')

    def form_valid(self, form):

        post = form.save(commit=False)

        if not self.request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/login/')

        if 'news/' in self.request.path and '/update' in self.request.path and post.p_type == 'AR':
            return HttpResponseRedirect('/posts/wrong_type_update/')

        elif 'articles/' in self.request.path and '/update' in self.request.path and post.p_type == 'NE':
            return HttpResponseRedirect('/posts/wrong_type_update/')

        return super().form_valid(form)


class PostDelete(PermissionRequiredMixin, DeleteView):

    permission_required = (
        'news.delete_post'
    )

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


class IndexView(View):

    def get(self, request):

        return render(request, 'welcome.html')


@login_required
def subscribe_ctg(request, id_ctg):

    user = request.user
    ctg = Category.objects.get(id=id_ctg)
    ctg.subscribers.add(user)

    return redirect(f'http://127.0.0.1:8000/posts/category/{id_ctg}')


@login_required
def unsubscribe_ctg(request, id_ctg):

    user = request.user
    ctg = Category.objects.get(id=id_ctg)
    ctg.subscribers.remove(user)

    return redirect(f'http://127.0.0.1:8000/posts/category/{id_ctg}')


def posts_by_category_list(request, id_ctg):

    posts = Post.objects.filter(categories__id=id_ctg).order_by('-post_date')
    is_subscribed = SubscribersCategory.objects.filter(user_id=request.user.pk, category_id=id_ctg).exists()
    cur_ctg = Category.objects.get(id=id_ctg)
    context = {
        'posts': posts,
        'cur_ctg': cur_ctg,
        'is_subscribed': is_subscribed
    }

    return render(request, 'posts_by_ctg.html', context=context)
