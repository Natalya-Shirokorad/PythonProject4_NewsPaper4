from datetime import datetime, timedelta, timezone
from django.core.mail import mail_managers, send_mail
from .models import Post, Category, User
from django.db.models.signals import post_save, post_delete, m2m_changed, pre_save
from django.dispatch import receiver # декоратор сигнала
from django.conf import settings
from django.core.exceptions import PermissionDenied #запрещение на определенные действия
from django.utils import timezone
import logging
from django.urls import reverse

# сигнал на уведомление о превышении возможности создавать более трех постов в сутки
@receiver(pre_save, sender=Post)
def post_limit_notifikation(sender, instance, **kwargs):
    if instance.pk:
        return
    before_datetime = timezone.now() - timedelta(days=1)
    posts_count = Post.objects.filter(author= instance.author, time_in__gte=before_datetime).count()
    if posts_count >= 3:
        raise PermissionDenied("Вы не можете создавать более трёх постов в сутки!")


# сигнал на уведомление на почту о подписке в определенной категории
@receiver(m2m_changed, sender=Category.subscribers.through)
def subscribers_notifikation(sender, instance, action, pk_set, **kwargs):
    if action =='post_add':
        user = User.objects.get(pk__in=pk_set)
        send_mail(
            subject='Новая подписка',
            message=f'Привет, {user.username}! Вы подписались на категорию  {instance.category_name}!'
            f'Список категорий ваших подписок: {", ".join(cat.category_name for cat in user.subscribed_categories.all())}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
    if action =='post_remove':
        user = User.objects.get(pk__in=pk_set)
        send_mail(
            subject = 'Вы отписались от категории',
            message=f'Привет, {user.username}! Вы отписались от категории {instance.category_name}!'
                    f'Список категорий ваших подписок: {", ".join(cat.category_name for cat in user.subscribed_categories.all())}',
            from_email = settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],

        )


# сигнал на уведомление на почту о новых публикациях в определенной категории
@receiver(m2m_changed, sender=Post.categorys.through)
def post_add_category(sender, instance, action, pk_set, **kwargs):
    if action!= 'post_add' or not pk_set:
        return
    try:
        # Получаем добавленные категории
        categories = Category.objects.filter(pk__in=pk_set)
        for category in categories:
            subscribers= category.subscribers.all()
            if not subscribers.exists():
                continue
            post_url = settings.SITE_URL + reverse('post_detail', args=[instance.id])
            send_mail(
                subject=f'Новая публикация в категории "{category.category_name}"',
                message=f'Вышла новая статья под названием "{instance.title}"\n Краткое содержание: {instance.text[:200]}...\n\n'
                        f'Читать польностью: {post_url} .\n\n'
                        f'\n Это письмо отправлено автоматически. Не отвечайте на него.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[subscriber.email for subscriber in subscribers if subscriber.email],
            )


    except Exception as e:
        print(f"Ошибка отправки уведомлений о новой публикации: {e}")

#
# Сигнал удаления публикаций
@receiver(post_delete, sender=Post)
def notify_about_post_deletion(sender, instance, **kwargs):
    subject = f'Автор {instance.author} удалил публикацию {instance.title}'

    mail_managers(
        subject=subject,
        message=f'Публикация {instance.title} удалена',
    )
    print(subject)