import os
from datetime import timedelta, date

from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from django.template.loader import render_to_string
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from requests import request

from .models import Post, SubscribersCategory, PostCategory
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def send_notifications(post, email, username):

    email_message = EmailMultiAlternatives(
        subject=f'{post.title}',
        body='',
        from_email=os.getenv('MAIN_EMAIL'),
        to=[email]
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


@receiver(m2m_changed, sender=Post.categories.through)
def send_email_post_created(sender, action, instance, **kwargs):

    if action == 'post_add':
        recipients = []
        # categories = PostCategory.objects.filter(post=instance.id).values('category')
        categories = instance.categories.all()

        if categories:
            for ctg in categories:
                # sub_set = SubscribersCategory.objects.filter(category=ctg.get('category')).values('user')
                sub_set = ctg.subscribers.all()

                if sub_set:
                    for sub in sub_set:
                        # us = User.objects.get(id=sub.get('user'))
                        if sub.email not in recipients:
                            recipients.append(sub.email)
                            send_notifications(instance, sub.email, sub.username)


@receiver(pre_save, sender=Post)
def add_posts_day_limit(sender, instance, **kwargs):

    today = timezone.now()
    quantity = Post.objects.filter(author=instance.author, post_date__date=today.date()).count()

    if quantity >= 3:
        return render(request, 'posts_day_limit.html')
