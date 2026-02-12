
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Author
from datetime import datetime
from .filters import PostFilter
from django.urls import reverse_lazy
from .forms import PostForm
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin, LoginRequiredMixin
from django.core.mail import send_mail
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import Group
from sign.utils import get_group
from sign.views import *
from django.core.mail import BadHeaderError


class PostList(ListView):
    model = Post
    post_type = None
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-time_in'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    paginate_by = 10  # вот так мы можем указать количество записей на странице

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
    # С помощью super() мы обращаемся к родительским классам
    # и вызываем у них метод get_context_data с теми же аргументами, что и были переданы нам.
    # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
    # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        context['next_posts'] = "Самые свежие новости в мире спорта смотрите на нашем сайте"
    # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельной статье или новости
    model = Post
    # Используем другой шаблон — post.html
    template_name = 'news_id.html'
    # Название объекта, в котором будет выбранный пользователем пост(статья или новость)
    context_object_name = 'news_id'


class NewsCreate(PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    # success_url = reverse_lazy('post_list') # Либо функцию в модель Пост def get_absolute_url(self) для возвращения на страницу новостей
    template_name = 'news/create.html'
    permission_required = 'news.add_post' # наделение прав создавать посты

    def form_valid(self, form):
        post = form.save(commit=False)
        if 'news' in self.request.path:
            post.article_or_news = 'NE'
        post.author = self.request.user.author  # Создаем автора
        # post.save()
        return super().form_valid(form)

class ArticlesCreate(PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    # success_url = reverse_lazy('post_list') # Либо функцию в модель Пост def get_absolute_url(self) для возвращения на страницу новостей
    template_name = 'articles/create.html'
    permission_required = 'news.add_post'



class NewsUpdate(PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/create.html'
    permission_required = 'news.change_post'

    def test_func(self):
        return self.get_object().author == self.request.user.author



class ArticlesUpdate(PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'articles/create.html'
    permission_required = 'news.change_post'

    def test_func(self):
        return self.get_object().author == self.request.user.author


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        return self.get_object().author == self.request.user.author

class ArticlesDelete(DeleteView):
    model = Post
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        return self.get_object().author == self.request.user.author


class SearchPostList(PostList):
    template_name = 'search.html'
    paginate_by = 5


class CategoryList(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'category/list_categories.html'
    context_object_name = 'categories'

@login_required
def subscribe(request, pk):
    category = Category.objects.get(pk=pk)
    category.subscribers.add(request.user)
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def unsubscribe(request, pk):
    category = Category.objects.get(pk=pk)
    category.subscribers.remove(request.user)
    return redirect(request.META.get('HTTP_REFERER'))


# функция для кнопки удаления новости с определенной публикации
def delete_news(request ):
    return render(request, 'news/news_delete.html')

# Вывод публикаций в определенной категории
def post_by_category(request, category_name):
    try:
        category= Category.objects.get(category_name=category_name)
        all_posts=Post.objects.filter(categorys__in=[category]).order_by('-time_in')
        # Создаем пагинатор
        paginator = Paginator(all_posts, 3)
        # Определяем текущую страницу из GET-запроса
        page_number=request.GET.get('page')
        posts = paginator.get_page(page_number)

    except Category.DoesNotExist:
        posts =None
    context = {'posts': posts, 'category_name':category_name }
    context['is_subscribers'] = request.user.groups.filter(name='subscribers').exists()
    return render(request, 'category/posts_by_category.html', context)


