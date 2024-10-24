from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView
from store.models import Category, Product, Tag


class ProductDetailView(TemplateView):
    template_name = 'shop-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Product, slug=kwargs.get('slug'))
        context['product'] = product
        return context


class HomePageView(TemplateView):
    template_name = 'index.html'


class CategoryAllView(TemplateView):
    template_name = 'shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = Tag.objects.all()
        products = Product.objects.all()
        tag = self.request.GET.get('tag', None)
        price = self.request.GET.get('rangeInput', None)

        if tag:
            products = products.filter(tags__name=tag)
        if price:
            try:
                price = float(price)
                products = products.filter(price__lte=price)
            except ValueError:
                pass

        query = self.request.GET.get('q')
        products = Product.objects.all()

        if query:
            products = products.filter(name__icontains=query)
        sort = self.request.GET.get('sort', '')

        if sort == 'price_asc':
            products = products.order_by('price')
        elif sort == 'price_desc':
            products = products.order_by('-price')
        elif sort == 'date_desc':
            products = products.order_by('-created_at')
        else:
            products = products.order_by('name')

        paginator = Paginator(products, 6)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        root_categories = Category.objects.filter(parent=None)
        context['tags'] = tags
        context['categories'] = root_categories
        context['products'] = products
        context['page_obj'] = page_obj
        return context


class CategoryListingView(TemplateView):
    template_name = 'shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = self.request.GET.get('tag', None)
        price = self.request.GET.get('rangeInput', None)
        category = get_object_or_404(Category, slug=kwargs.get('slug'))
        query = self.request.GET.get('q')
        products = Product.objects.all()

        if query:
            products = products.filter(name__icontains=query, category=category)
        else:
            products = Product.objects.filter(category=category)
        sort = self.request.GET.get('sort', '')
        if tag:
            products = products.filter(tags__name=tag)
        if price:
            try:
                price = float(price)
                products = products.filter(price__lte=price)
            except ValueError:
                pass



        if sort == 'price_asc':
            products = products.order_by('price')
        elif sort == 'price_desc':
            products = products.order_by('-price')
        elif sort == 'date_desc':
            products = products.order_by('-created_at')
        else:
            products = products.order_by('name')

        paginator = Paginator(products, 6)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['tags'] = Tag.objects.all()
        context['category'] = category
        context['child_categories'] = category.children.all()
        context['products'] = products
        context['page_obj'] = page_obj
        context['']

        return context


class ContactView(TemplateView):
    template_name = 'contact.html'


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {
            'name': product.name,
            'price': product.price,
            'quantity': 1,
            'image': product.image.url
        }

    request.session['cart'] = cart
    return redirect('cart')
