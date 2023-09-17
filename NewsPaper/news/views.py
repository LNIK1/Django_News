import os
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, Category, SubscribersCategory, PostCategory
from .filters import PostFilter
from .forms import PostForm
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class PostList(ListView):

    model = Post
    queryset = Post.objects.order_by('-post_date')
    template_name = 'posts.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        return context


class PostDetail(DetailView):

    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


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

        if 'news/create' in self.request.path:
            post.p_type = 'NE'
        elif 'articles/create' in self.request.path:
            post.p_type = 'AR'

        send_email_post_created(post, self.request.user.username)

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


def send_email_post_created(post, username):

    recipients = []
    categories = PostCategory.objects.filter(post=post).values('category')
    for ctg in categories:
        sub_set = SubscribersCategory.objects.filter(category=ctg.get('category'))
        for sub in sub_set:
            if sub.user.email not in recipients:
                recipients.append(sub.user.email)

    email_message = EmailMultiAlternatives(
        subject=f'{post.title}',
        body=f'Здравствуй, {username}. Новая статья в твоем любимом разделе !\n\n'
             f'{post.title}\n{post.text[:50]}...',
        from_email=os.getenv('MAIN_EMAIL'),
        to=recipients
    )

    html_content = render_to_string(
        'email_content.html',
        {
            'post': post,
            'username': username
         }
    )

    email_message.attach_alternative(html_content, 'text/html')
    email_message.send()
