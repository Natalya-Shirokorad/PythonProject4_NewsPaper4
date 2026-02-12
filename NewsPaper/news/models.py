
from django.db import models
from datetime import datetime
from django.utils import timezone
from .resources import AUTHOR_CHOICES, ARTICLE
from django.contrib.auth.models import User
from django.urls import reverse

from django.core.exceptions import ObjectDoesNotExist

   # --- Модель Category ---
class Category(models.Model):  # Категории новостей/статей — темы, которые они отражают (спорт, политика, образование и т. д.).
    category_name = models.CharField(max_length=50, unique=True, verbose_name="Название категории")
    subscribers = models.ManyToManyField(User, blank=True, related_name="subscribed_categories" , verbose_name="Подписки на категории")


    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


 # --- Модель Author ---
class Author(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    rating = models.FloatField(default=0.0, verbose_name="Рейтинг автора")
    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Список авторов"
    def update_rating(self):
# 1. Суммарный рейтинг каждой статьи автора умножается на 3
        post_ratings = 0
        for post in self.post_set.all():  # Используем post_set для получения всех постов автора
            post_ratings += post.rating * 3
#
# 2. Суммарный рейтинг всех комментариев автора
        comment_rating_by_author = 0
        for comment in Comment.objects.filter(user=self.user):
            comment_rating_by_author += comment.comment_rating

# 3. Суммарный рейтинг всех комментариев к статьям автора
        comments_to_posts_ratings = 0
        for post in self.post_set.all():
            for comment in post.comment_set.all():  # Для каждого поста автора, суммируем рейтинги его комментариев
                comments_to_posts_ratings += comment.comment_rating

# Обновляем общий рейтинг автора
        self.rating = post_ratings + comment_rating_by_author + comments_to_posts_ratings
        self.save()

    def __str__(self):
        return self.user.username


# --- Модель Post ---
class Post(models.Model): # Модель Пост. Эта модель должна содержать в себе статьи и новости, которые создают пользователи.
    # Каждый объект может иметь одну или несколько категорий.
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор") #	связь «один ко многим» с моделью Author
    article_or_news = models.CharField(choices=AUTHOR_CHOICES, default=ARTICLE, verbose_name="Тип записи") # статья или новость. По умолчанию новость
    time_in = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")   # автоматически добавляемая дата и время создания
    title = models.CharField(max_length = 100, verbose_name="Заголовок")    # 	заголовок статьи/новости;
    text = models.TextField(verbose_name="Текст")           #	текст статьи/новости
    rating = models.IntegerField(default= 0, verbose_name="Рейтинг записи")  #	рейтинг статьи/новости.
    categorys = models.ManyToManyField(Category, through='PostCategory', verbose_name="Категории", related_name="categories_post")
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    # category = models.ForeignKey(Category)
    #связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory)


    def __str__(self):
        return (f'{self.title}'
                f'{self.text}'
                f'({self.get_article_or_news_display()})')

    def like_post(self):
# Увеличивает рейтинг записи на 1
        self.rating += 1
        self.save()
        # return self.rating

    def dislike_post(self):
# Уменьшает рейтинг записи на 1
        self.rating -= 1
        self.save()
        # return self.rating

    def preview(self): #возвращает начало статьи (предварительный просмотр) длиной 124 символа и добавляет многоточие в конце
        if len(self.text) > 124:
            return self.text[:124] + '...'
        return self.text
    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Новости и Статьи"

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

# --- Модель PostCategory ---
class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)

    def __str__(self):
        return f'{self.post.title} -> {self.category.category_name}'
    # Связь «один ко многим» с моделью Post

# --- Модель Comment ---
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text_comment = models.TextField()  # Текст комментария
    time_in_category = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default= 0)  # рейтинг комментария

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def like(self):
        self.comment_rating += 1
        self.save()
        return self.comment_rating

    def dislike(self):
        self.comment_rating -= 1
        self.save()
        return self.comment_rating


    def __str__(self):
        return f'Комментарий от {self.user.username}  к "{self.post.title}"'