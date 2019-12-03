from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

import views


urlpatterns = [
    path('', views.index, name='miggi'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
  urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
