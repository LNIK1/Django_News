import os
import datetime

from celery import shared_task

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Category, SubscribersCategory, PostCategory
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


@shared_task
def send_email_weekly_posts():

    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)

    posts = Post.objects.filter(post_date__gte=last_week)
    categories = list(set(posts.values_list('categories__name', flat=True)))
    subscribers = list(set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True)))

    if '' in subscribers:
        subscribers.pop(subscribers.index(''))

    html_content = render_to_string(
        'weekly_posts.html',
        {
            'link': f'http://127.0.0.1:8000/posts/',
            'posts': posts
        }
    )

    msg = EmailMultiAlternatives(
        subject='Посты за прошлую неделю',
        body='',
        from_email=os.getenv('MAIN_EMAIL'),
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def send_email_post_created(id_post):

    # if action == 'post_add':
    recipients = []
    post = Post.objects.get(id=id_post)
    # categories = PostCategory.objects.filter(post=id_post).values('category')
    categories = post.categories.all()

    if categories:
        for ctg in categories:
            # sub_set = SubscribersCategory.objects.filter(category=ctg.get('category')).values('user')
            sub_set = ctg.subscribers.all()

            if sub_set:
                for sub in sub_set:
                    # us = User.objects.get(id=sub.get('user'))
                    if sub.email not in recipients:
                        recipients.append(sub.email)

                        email_message = EmailMultiAlternatives(
                            subject=f'{post.title}',
                            body='',
                            from_email=os.getenv('MAIN_EMAIL'),
                            to=[sub.email]
                        )

                        html_content = render_to_string(
                            'email_content.html',
                            {
                                'post': post,
                                'username': sub.username,
                                'link': f'http://127.0.0.1:8000/posts/{id_post}'
                            }
                        )

                        email_message.attach_alternative(html_content, 'text/html')
                        email_message.send()
