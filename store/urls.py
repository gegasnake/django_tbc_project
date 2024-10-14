from django.conf.urls.static import static
from django.urls import path

from django_tbc_project import settings
from .views import CategoryListView, ProductListView, ProductDetailView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:category_id>/products/', ProductListView.as_view(), name='category-by-products'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),  # New URL for product detail
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # this is an endpoint I added to serve media files
    # However, I always use this for development, not for production because nginx has its own ways to work with
    # media files
