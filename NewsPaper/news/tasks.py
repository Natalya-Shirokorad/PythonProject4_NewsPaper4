from datetime import timezone

from celery import shared_task
from django.core.mail import send_mail
from django.urls import reverse
from NewsPaper import settings
from .models import Post, Category
from django.utils import timezone
from datetime import timedelta

# Pассылкa уведомлений подписчикам после создания новости без form.save_m2m() в form_valid не работает.
@shared_task
def create_new_post(post_id, **kwargs):
    post = Post.objects.get(pk = post_id)
    categories = post.categorys.all()
    if not categories.exists():
        print(f"Пост {post_id} не имеет категорий")
        return
    for categori in categories:
        subscribers = categori.subscribers.all()
        if not subscribers.exists():
            print(f"Категория {categori.category_name} не имеет подписчиков")
            continue
        post_url = settings.SITE_URL + reverse('post_detail', args=[post.id])
        recipient_list = [subscriber.email for subscriber in subscribers if subscriber.email]
        if not recipient_list:
            print(f"Нет валидных email в категории {categori.category_name}")
            continue
        send_mail(
            subject=f'Новая публикация в категории "{categori.category_name}"',
            message=f'Вышла новая статья под названием "{post.title}"\n Краткое содержание: {post.text[:200]}...\n\n'
                    f'Читать польностью: {post_url} .\n\n'
                    f'\n Это письмо отправлено автоматически. Не отвечайте на него.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
        )
        print(f"Отправлено уведомление для категории {categori.category_name} "
              f"({len(recipient_list)} подписчиков)")


# Eженедельная рассылка с последними новостями (каждый понедельник в 8:00 утра).
@shared_task
def sending_out_posts_for_the_previous_week():
    categories = Category.objects.all()  # список категорий
    week_ago = timezone.now() - timedelta(days=7)  # промежуток времени равен 7 дням

    for category in categories:
        subscribers = category.subscribers.all()
        if not subscribers.exists():
            continue

        week_posts = Post.objects.filter(categorys=category,
                                         time_in__gte=week_ago).distinct()  # Посты за неделю по категориям
        if not week_posts.exists():  # если нет новых постов в этой категории за неделю прерываем
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

        #  Логика рассылки...
        print(f"Отправлена рассылка для категории '{category.category_name}' "
              f"({week_posts.count()} постов, {len(recipient_list)} подписчиков)")
