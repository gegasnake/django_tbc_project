from django.urls import path


from .views import ProductDetailView, HomePageView, CategoryListingView, ContactView, CategoryAllView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('category/', CategoryAllView.as_view(), name='category'),
    path('category/<slug:slug>/', CategoryListingView.as_view(), name='category_listing'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('contact/', ContactView.as_view(), name='contact'),
]

