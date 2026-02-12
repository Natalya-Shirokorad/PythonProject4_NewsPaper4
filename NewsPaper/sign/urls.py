from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import confirm_logout, my_profile, be_author
# from .views import BaseRegisterView
from .views import upgrade_me
from .views import SignUpView
from .views import add_author_to_group
from .views import be_subscribers


urlpatterns = [
    path('login/',
         LoginView.as_view(template_name ='sign/login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name ='sign/logout.html'),
         name='logout'),
    path('confirm/logout/', confirm_logout, name='confirm_logout'),  # Путь уточнение на выход из системы
    # Путь для подключения регистрации через models.py
    # path('signup/',
    #      BaseRegisterView.as_view(template_name = 'sign/signup.html'),
    #      name='signup'),
    path('signup/', SignUpView.as_view(template_name = 'sign/signup.html'),
         name='signup'),
    path('profile/', my_profile, name ='profile'),
    path('upgrade/', upgrade_me, name ='upgrade'), # Путь к добавить в группу Премиум
    path('authors/', add_author_to_group, name ='authors'), # Путь к добавить в группу Автор
    path('be_author/', be_author, name ='be_author'), # Путь добавить группу и стать автором
    path('be_subscribers/', be_subscribers, name ='be_subscribers'), # Путь добавления в группу subscribers
]
