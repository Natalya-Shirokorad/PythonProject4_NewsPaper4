from django.urls import path
# Импортируем созданное нами представление
from .views import (PostList, PostDetail, NewsCreate, NewsUpdate, ArticlesUpdate, NewsDelete,
                    ArticlesDelete, SearchPostList, CategoryList)
from .views import delete_news
from .views import post_by_category
from .views import subscribe, unsubscribe




urlpatterns = [
   path('', PostList.as_view(), name= 'post_list'),
   path('search/', SearchPostList.as_view(), name= 'search_post_list'),
   path('<int:pk>', PostDetail.as_view(), name = 'post_detail'),
   path('news/create/', NewsCreate.as_view(template_name= 'news/create.html'), name='news_create'),
   path('articles/create/', NewsCreate.as_view(template_name= 'articles/create.html'), name='articles_create'),
   path('news/<int:pk>/update/', NewsUpdate.as_view(template_name= 'news/create.html'), name='news_update'),
   path('articles/<int:pk>/update/', ArticlesUpdate.as_view(template_name= 'articles/create.html'), name='articles_update'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(template_name= 'news/news_delete.html'), name='news_delete' ),
   path('articles/<int:pk>/delete/', ArticlesDelete.as_view(template_name= 'articles/articles_delete.html'), name='articles_delete'),
   path('delete/news/', delete_news, name='delete_news'),
   path('category/<str:category_name>/', post_by_category, name='post_by_category'), # путь к публикациям по названию категории спорт
   path('categories/', CategoryList.as_view(), name='categories_list'), # путь к списку всех категорий
   path('category/<int:pk>/subscribe/', subscribe, name='subscribe'),
   path('category/<int:pk>/unsubscribe/', unsubscribe, name='unsubscribe'),
   # path('subscribers', subscribers, name='subscribers'),
   # path('subscribe/<str:category_name>/', views.subscribe_to_category, name='subscribe_to_category'),

]




