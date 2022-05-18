import logging
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import send_mail
from datetime import datetime
from news.models import Category, Post


logger = logging.getLogger(__name__)



def news_sender():
    for category in Category.objects.all():
        news_from_each_category = []
        week_number_last = datetime.now().isocalendar()[1] - 1
        for news in Post.objects.filter(postCategory=category.id,
                                        dateCreation__week=week_number_last).values('pk',
                                                                                    'title',
                                                                                    'dateCreation',
                                                                                    'postCategory__name'):
            # print("category.id:", category.id)
            date_format = news.get("dateCreation").strftime("%d/%m/%Y")
            new = (f'{news.get("title")}, Категория: {category.name}. '
                   f'Дата создания: {date_format}. Ссылка - http://127.0.0.1:8000/news/{news.get("pk")}')
            # print('new=', new)
            news_from_each_category.append(new)
            # print('news_from_each_category=', news_from_each_category)
            

        subscribers = category.subscribers.all()
        for subscriber in subscribers:
            

            send_mail(
                subject=f'Новинки недели в рубрике {category.name}',
                message=f"Здравствуйте, {subscriber.username}. "
                        f' Публикации за неделю:\n {news_from_each_category} \n'
                        f'До встречи на нашем сайте!',
                from_email='imya6301@yandex.ru',
                recipient_list=[subscriber.email]
            )


def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            news_sender,

            # для проверки отправки временно задано время срабатывания каждые 15 секунд
            trigger=CronTrigger(second="*/15"),
            # Ниже тригер для еженедельной рассылки
            # trigger=CronTrigger(day_of_week="mon", hour="08", minute="00"),

            id="news_sender",  
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Добавлена работка 'news_sender'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),

            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Шедулер запущен")
            print('Шедулер запущен')
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Шедулер остановлен")
            scheduler.shutdown()
            print('Шедулер остановлен')
            logger.info("Шедулер остановлен успешно!")