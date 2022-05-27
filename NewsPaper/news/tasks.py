from celery import shared_task
import time
from django.core.mail import send_mail
from datetime import datetime
from news.models import Category, Post
from celery.schedules import crontab

# import instance


@shared_task
def send_post_create_celery():
    for user_id in users:
        send_mail(
            subject=f'Celery. Новая публикация - "{instance.title}"',
            message=f"Здравствуй, {User.objects.get(pk=user_id['subscribers']).username}. "
                    f'Новая публикация в вашем любимом разделе! \n"{instance.text[:50]}..."\n'
                    f'Пройдите по ссылке {link} что бы прочитать на нашем сайте.',
            from_email='imya6301@yandex.ru',
            recipient_list=[User.objects.get(pk=user_id['subscribers']).email]
        )
    
@shared_task
def send_mail_for_sub_every_week():
    for category in Category.objects.all():
        news_from_each_category = []
        week_number_last = datetime.now().isocalendar()[1] - 1
        for news in Post.objects.filter(postCategory=category.id,
                                        dateCreation__week=week_number_last).values('pk',
                                                                                    'title',
                                                                                    'dateCreation',
                                                                                    'postCategory__name'):
            date_format = news.get("dateCreation").strftime("%d/%m/%Y")
            new = (f'{news.get("title")}, Категория: {category.name}. '
                   f'Дата создания: {date_format}. Ссылка - http://127.0.0.1:8000/news/{news.get("pk")}')
            news_from_each_category.append(new)

        subscribers = category.subscribers.all()
        if news_from_each_category:

            for subscriber in subscribers:
                send_mail(
                    subject=f'Celery. Новинки недели в рубрике {category.name}',
                    message=f"Здравствуйте, {subscriber.username}. "
                            f' Публикации за неделю:\n {news_from_each_category} \n'
                            f'До встречи на нашем сайте!',
                    from_email='imya6301@yandex.ru',
                    recipient_list=[subscriber.email]
                )