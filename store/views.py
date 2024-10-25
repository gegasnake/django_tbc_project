from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import TemplateView

from order.models import Cart, CartItem
from store.models import Category, Product, Tag


class HomePageView(TemplateView):
    template_name = 'index.html'


class ProductDetailView(TemplateView):
    template_name = 'shop-detail.html'


class ContactView(TemplateView):
    template_name = 'contact.html'



class ProductListView(TemplateView):
    template_name = 'shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = Tag.objects.all()
        products = Product.objects.all()
        category_slug = kwargs.get('slug')
        category = None

        # Filter by category if slug is given
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)

        # Filter by search query
        query = self.request.GET.get('search_bar')
        if query:
            products = products.filter(name__icontains=query)

        # Filter by tag
        tag = self.request.GET.get('tag')
        if tag:
            products = products.filter(tags__name=tag)

        # Filter by price
        price = self.request.GET.get('rangeInput')
        if price:
            try:
                price = float(price)
                products = products.filter(price__lte=price)
            except ValueError:
                pass

        # Sort products based on the `sort` parameter
        sort = self.request.GET.get('sort', '')
        if sort == 'price_asc':
            products = products.order_by('price')
        elif sort == 'price_desc':
            products = products.order_by('-price')
        elif sort == 'date_desc':
            products = products.order_by('-created_at')
        else:
            products = products.order_by('name')

        # Pagination
        paginator = Paginator(products, 6)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        root_categories = Category.objects.filter(parent=None)
        context.update({
            'tags': tags,
            'categories': root_categories,
            'category': category,
            'child_categories': category.children.all() if category else None,
            'products': products,
            'page_obj': page_obj,
        })
        return context


class CartView(View):
    template_name = 'cart.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Authenticated user's cart
            cart, _ = Cart.objects.get_or_create(user=request.user)
            cart_items = cart.items.all()
            cart_items_with_total = [
                {
                    'item': item,
                    'total_price': item.product.price * item.quantity
                }
                for item in cart_items
            ]
            total_price = sum(item['total_price'] for item in cart_items_with_total)
        else:
            # Anonymous user's cart from session
            session_cart = request.session.get('cart', {})
            cart_items_with_total = []
            total_price = 0
            for product_id, quantity in session_cart.items():
                product = get_object_or_404(Product, id=product_id)
                total_price += product.price * quantity
                cart_items_with_total.append({
                    'item': {'product': product, 'quantity': quantity},
                    'total_price': product.price * quantity
                })

        return render(request, self.template_name, {
            'cart_items_with_total': cart_items_with_total,
            'total_price': total_price,
        })

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity", 1))
        action = request.POST.get("action")

        if request.user.is_authenticated:
            # For authenticated users we use with database cart
            cart, _ = Cart.objects.get_or_create(user=request.user)
            product = get_object_or_404(Product, id=product_id)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

            # Handle cart actions
            if action == "add":
                cart_item.quantity = quantity if created else cart_item.quantity + quantity
                cart_item.save()
            elif action == "increase":
                cart_item.quantity += 1
                cart_item.save()
            elif action == "decrease":
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                else:
                    cart_item.delete()
            elif action == "remove":
                cart_item.delete()
        else:
            # For anonymous users, store in session
            session_cart = request.session.get('cart', {})
            if action == "add":
                session_cart[product_id] = session_cart.get(product_id, 0) + quantity
            elif action == "increase":
                session_cart[product_id] = session_cart.get(product_id, 0) + 1
            elif action == "decrease":
                if session_cart.get(product_id, 0) > 1:
                    session_cart[product_id] -= 1
                else:
                    session_cart.pop(product_id, None)
            elif action == "remove":
                session_cart.pop(product_id, None)

            # I am saving the cart in session
            request.session['cart'] = session_cart

        return redirect('cart')
