"""
URL configuration for django_tbc_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django_tbc_project import settings
from django.conf.urls.static import static
from store.views import custom_404_view, custom_500_view
from django.conf.urls import handler404, handler500

urlpatterns = [
    path('store/', include('store.urls')),
    path('order/', include('order.urls')),
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('rosetta/', include('rosetta.urls')),

]

handler404 = custom_404_view
handler500 = custom_500_view

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # this is an endpoint I added to serve media files
    # However, I always use this for development, not for production because nginx has its own ways to work with
    # media files
