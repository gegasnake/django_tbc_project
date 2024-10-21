# from django.db.models import Avg, Sum
# from django.shortcuts import render, get_object_or_404
# from django.views import View
# from .models import Category, Product
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView

from store.models import Category, Product


class ProductDetailView(TemplateView):
    template_name = 'shop-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Product, slug=kwargs.get('slug'))  # Get the product by its slug
        context['product'] = product  # Pass the product to the template context
        return context


class HomePageView(TemplateView):
    template_name = 'index.html'


class CategoryListingView(TemplateView):
    template_name = 'shop.html'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, slug=kwargs.get('slug'))
        context['category'] = category
        # context['products'] = Product.objects.filter(category=category)
        return context



class ContactView(TemplateView):
    template_name = 'contact.html'




# class CategoryListView(View):
#     def get(self, request, *args, **kwargs):
#         categories = Category.objects.filter(parent__isnull=True)
#
#         # I am getting all categories with its children and its parent
#         category_data = [
#             {
#                 'id': category.id,
#                 'name': category.name,
#                 'parent': [category.parent.id, category.parent.name] if category.parent is not None else None,
#                 'children': [child.name for child in category.get_children()],
#                 'product_count': category.get_product_count(),
#             }
#             for category in categories
#         ]
#         return render(request, 'base.html', {'category_data': category_data})
#
#
# class ProductListView(View):
#     def get(self, request, category_id, *args, **kwargs):
#         category = get_object_or_404(Category, id=category_id)
#         subcategories = category.get_children()
#         products = Product.objects.filter(categories__in=[category] + list(subcategories))
#         product_data = [
#             {
#                 'id': product.id,
#                 'name': product.name,
#                 'image': request.build_absolute_uri(product.image.url) if product.image and
#                                                                           product.image.name else None,
#                 'sum': product.price * product.quantity,
#             }
#             for product in products
#         ]
#         most_expensive_price = products.order_by('price').last().price
#         most_cheap_price = products.order_by('price').first().price
#         avg_price = products.aggregate(Avg('price'))['price__avg']
#         all_sum_price = sum([p.price * p.quantity for p in products])
#
#         return render(request, 'base.html',
#                       {'product_data': product_data,
#                                'max_price': most_expensive_price,
#                                'min_price': most_cheap_price,
#                                'avg_price': avg_price,
#                                'all_sum_price': all_sum_price,
#                        })
#