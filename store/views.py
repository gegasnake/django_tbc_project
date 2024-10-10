from django.http import JsonResponse
from django.views import View
from .models import Category, Product


class CategoryListView(View):
    def get(self, request, *args, **kwargs):
        # a category may not have a parent, therefore, it will be null and I filter it so it fatches only those.
        categories = Category.objects.filter(parent__isnull=True)
        # getting every category with its children
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
                'categories': [{'id': category.id, 'name': category.name} for category in product.categories.all()]
            }
            for product in products
        ]
        return JsonResponse(product_data, safe=False)
