from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_home, name='order_home'),
    path('details/', views.order_details, name='order_details'),
]
