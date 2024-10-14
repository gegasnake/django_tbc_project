from django.urls import path


from .views import CategoryListView, ProductListView, ProductDetailView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:category_id>/products/', ProductListView.as_view(), name='category-by-products'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),  # New URL for product detail
]

