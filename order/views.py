from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from store.models import Category


class CartView(TemplateView):
    model = Category
    query_pk_and_slug = 'slug'
    template_name = 'cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        return context


class CheckoutView(TemplateView):
    template_name = 'chackout.html'
