import logging
from datetime import timedelta

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution


from news.models import Post, Category, User
from django.urls import reverse

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
    categories = Category.objects.all() #список категорий
    week_ago = timezone.now() - timedelta(days=7) #  промежуток времени равен 7 дням

    for category in categories:
        subscribers = category.subscribers.all()
        if not subscribers.exists():
            continue

        week_posts = Post.objects.filter(categorys = category,
        time_in__gte=week_ago).distinct()  # Посты за неделю по категориям
        if not week_posts.exists(): # если нет новых постов в этой категории за неделю прерываем
            continue

        # Формируем список получателей
        recipient_list = [subscriber.email for subscriber in subscribers if subscriber.email]
        if not recipient_list:
            continue

        # Формируем текст письма с ссылками на все посты
        text_for_message = ""
        for post in week_posts:
            post_url = settings.SITE_URL + reverse('post_detail', args=[post.id])
            text_for_message += f'\n {post.title[:100]}... \n {post_url}\n'


        send_mail(
            subject=f'Новые публикация в категории "{category.category_name}" за неделю.',

            message=f'Добрый день! За прошедшую неделю в категории "{category.category_name}" вышли новые публикации: {text_for_message}"\n\n'
                f'Всего вышло публикаций: {week_posts.count()} .\n\n'
                    
                f'\n Это письмо отправлено автоматически. Не отвечайте на него.',

            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
        )

    #  Your job processing logic here...
        print(f"Отправлена рассылка для категории '{category.category_name}' "
            f"({week_posts.count()} постов, {len(recipient_list)} подписчиков)")


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            # Запускать каждый понедельник в 10:00 утра
            trigger=CronTrigger(
                day_of_week="mon",  # Понедельник
                hour="10",  # 10 часов
                minute="00"  # 00 минут
            ),
            # trigger=CronTrigger(second="*/59"),
            # # То же, что и интервал, но задача тригера таким образом более понятна django
            id="weekly_newsletter",  # Позже можем найти задачу по id job = scheduler.get_job("weekly_newsletter")
            # Или удалить задачу по id scheduler.remove_job("weekly_newsletter")
            # Или изменить параметры задачи scheduler.modify_job("weekly_newsletter", trigger=CronTrigger(hour="12"))
            max_instances=1,
            replace_existing=True,
            #Без replace_existing=True при повторном добавлении задачи с тем же id будет ошибка
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")