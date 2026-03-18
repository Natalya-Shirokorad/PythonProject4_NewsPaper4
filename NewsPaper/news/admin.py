from django.contrib import admin
from .models import (Category, Author, Post, PostCategory,
                     Comment)


# создаём новый класс для представления товаров в админке
class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    # list_display = [field.name for field in
    #                 Post._meta.get_fields()]  # генерируем список имён всех полей для более красивого отображения
    list_display = ('title', 'author', 'time_in')  # оставляем только имя и цену товара
    list_filter = ('title', 'author' )  # добавляем примитивные фильтры в нашу админку
    search_fields = ('title', 'article_or_news')  # тут всё очень похоже на фильтры из запросов в базу


# Register your models here.

admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(PostCategory)
admin.site.register(Comment)