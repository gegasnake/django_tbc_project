from django.http import JsonResponse
from django.views import View
from .models import Category, Product


class CategoryListView(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.filter()
        # I am getting all categories with its children
        category_data = [
            {
                'id': category.id,
                'name': category.name,
                'children': [{'id': child.id, 'name': child.name} for child in category.children.all()]
            }
            for category in categories
        ]
        return JsonResponse(category_data, safe=False)


class ProductListView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        # getting all products with loop
        # it does pretty same things like Category view but it shows us all products.
        product_data = [
            {
                'id': product.id,
                'name': product.name,
                'image': "http://127.0.0.1:8000" + product.image.url,
                'categories': [{'id': category.parent.id, 'name': category.parent.name}
                               for category in product.categories.all()]
            }
            for product in products
        ]
        return JsonResponse(product_data, safe=False)
