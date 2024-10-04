from django.urls import path
from . import views

urlpatterns = [
    path('', views.store_home, name='store_home'),
    path('products/', views.product_list, name='product_list'),
]
