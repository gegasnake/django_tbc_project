from django.db.models import Avg, Sum
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Category, Product


class CategoryListView(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.filter(parent__isnull=True)

        # I am getting all categories with its children and its parent
        category_data = [
            {
                'id': category.id,
                'name': category.name,
                'parent': [category.parent.id, category.parent.name] if category.parent is not None else None,
                'children': [child.name for child in category.get_children()],
                'product_count': category.get_product_count(),
            }
            for category in categories
        ]
        return render(request, 'category.html', {'category_data': category_data})


class ProductListView(View):
    def get(self, request, category_id, *args, **kwargs):
        category = get_object_or_404(Category, id=category_id)
        subcategories = category.get_children()
        products = Product.objects.filter(categories__in=[category] + list(subcategories))
        product_data = [
            {
                'id': product.id,
                'name': product.name,
                'image': request.build_absolute_uri(product.image.url) if product.image and
                                                                          product.image.name else None,
                'sum': product.price * product.quantity,
            }
            for product in products
        ]
        most_expensive_price = products.order_by('price').last().price
        most_cheap_price = products.order_by('price').first().price
        avg_price = products.aggregate(Avg('price'))['price__avg']
        all_sum_price = sum([p.price * p.quantity for p in products])

        return render(request, 'products_by_category.html',
                      {'product_data': product_data,
                               'max_price': most_expensive_price,
                               'min_price': most_cheap_price,
                               'avg_price': avg_price,
                               'all_sum_price': all_sum_price,
                       })


class ProductDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        total_value = product.quantity * product.price
        return render(request, 'details_of_product.html', {'product': product,
                                                           'total_value': total_value})
