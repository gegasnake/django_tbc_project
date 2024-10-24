from django.urls import path
from .views import CheckoutView
from store.views import add_to_cart

urlpatterns = [
    path('cart/', add_to_cart, name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]
