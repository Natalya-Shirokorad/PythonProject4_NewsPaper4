from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
# from .models import BaseRegisterForm
from .forms import SignUpForm
from django.urls import reverse_lazy

from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from news.models import Author, Category
from .utils import get_group


def confirm_logout(request):
    return render(request, 'sign/confirm_logout.html')

# class BaseRegisterView(CreateView):  # 1 способ регистрация на сайте с применением models.py
#     model = User
#     form_class = BaseRegisterForm
#     success_url = '/'


class SignUpView(CreateView):   # 2 способ регистрация на сайте с применением forms.py
    model = User
    template_name = 'sign/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('index')

@login_required
def add_author_to_group(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    else:
        author_group.user_set.remove(user)
    return redirect('/')

@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='premium')
    if not request.user.groups.filter(name='premium').exists():
        premium_group.user_set.add(user)
    return redirect('category/<str:category_name>/')

@login_required
def my_profile(request):
    # user = request.user   #функция для перенаправления на страничку зарег. пользователя.
    context= {'is_author':request.user.groups.filter(name='authors').exists(),
              'is_subscribers':request.user.groups.filter(name='subscribers').exists()} # для выявления подписки в группу.
               # 'if_the_author_changes':request.user.groups.filter(name='authors').exists(),}# context для проверки находится ли пользователь в группе автор.
    return render(request, 'protect/index.html', context)

# функция для прооверки относится ли зарег. пользователь к группе автор. Если такой группы нет, то создается.
@login_required
def be_author(request):
    Author.objects.get_or_create(user=request.user)
    group_authors = get_group('authors')

    if not request.user.groups.filter(name='authors').exists():
        request.user.groups.add(group_authors)
        list(messages.get_messages(request))
        messages.success(
            request, "Поздравляем! Вы стали автором!",
            extra_tags='authors'
        )

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def be_subscribers(request):
    current_user = request.user
    # Author.objects.get(user=request.user)
    group_subscribers = get_group('subscribers')

    if not current_user.groups.filter(name='subscribers').exists():
        current_user.groups.add(group_subscribers)
        # category = Category.objects.get(category_name='sports')
        # category.subscribers.add(current_user)
        list(messages.get_messages(request))
        messages.success(
            request, "Вы подписаны на рассылку обновления публикаций в группе 'subscribers'",
            extra_tags = 'subscribers'
        )
    else:
        # category = Category.objects.get(category_name='sports')
        # category.subscribers.remove(current_user)
        current_user.groups.remove(group_subscribers)
        list(messages.get_messages(request))
        messages.success(
            request, "Вы отписались от уведомлений об обновлениях публикаций в группе  'subscribers'",
            extra_tags='unsubscribers')



