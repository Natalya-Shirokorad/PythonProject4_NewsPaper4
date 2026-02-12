from django.urls import path
from .views import IndexView


urlpatterns = [
    path('index/', IndexView.as_view(template_name='protect/index.html'),
         name='index'),
]