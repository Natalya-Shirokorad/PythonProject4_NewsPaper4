
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
 #Добаление картинки на страницу сайта.
from django.conf import settings
from django.conf.urls.static import static
#-------------------------------------------


urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('', include('news.urls')),
    path('protect/', include('protect.urls')),
    path('sign/', include('sign.urls')),
    path('accounts/', include('allauth.urls')),
    # path('appointments/', include('appointments.urls')),
    path('appointments/', include(('appointments.urls', 'appointments'), namespace='appointments')),
]

# Добаление картинки на страницу сайта.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#--------------------------------------------------------------------