from django.conf.urls.static import static
from django.urls import path

from django_tbc_project import settings
from .views import CategoryListView, ProductListView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('products/', ProductListView.as_view(), name='product-list'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # this is an endpoint I added to serve media files
    # However, I always use this for development, not for production because nginx has its own ways to work with
    # media files
