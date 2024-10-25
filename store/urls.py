from django.urls import path


from .views import ProductDetailView, HomePageView, ContactView, ProductListView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('category/', ProductListView.as_view(), name='category'),
    path('category/<slug:slug>/', ProductListView.as_view(), name='category_listing'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('contact/', ContactView.as_view(), name='contact'),
]

