import os

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import Post, SubscribersCategory, PostCategory
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


@receiver(post_save, sender=Post)
def send_email_post_created(sender, instance, created, **kwargs):

    recipients = []
    categories = PostCategory.objects.filter(post=instance).values('category')
    # categories = instance.categories.all()

    if categories:
        for ctg in categories:
            sub_set = SubscribersCategory.objects.filter(category=ctg.get('category')).values('user')
            # sub_set = ctg.subscribers.all()

            if sub_set:
                for sub in sub_set:
                    us = User.objects.get(id=sub.get('user'))
                    if us.email not in recipients:
                        recipients.append(us.email)

    email_message = EmailMultiAlternatives(
        subject=f'{instance.title}',
        body=f'Здравствуйте, . Новая статья в твоем любимом разделе !\n\n'
             f'{instance.title}\n{instance.text[:50]}...',
        from_email=os.getenv('MAIN_EMAIL'),
        to=recipients
    )

    html_content = render_to_string(
        'email_content.html',
        {
            'post': instance,
            # 'username': username
         }
    )

    email_message.attach_alternative(html_content, 'text/html')
    email_message.send()
