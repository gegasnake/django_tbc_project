from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView

from order.models import Cart, CartItem
from store.models import Product


@method_decorator(login_required, name='dispatch')
class CheckoutView(TemplateView):
    template_name = 'chackout.html'


@method_decorator(login_required, name='dispatch')
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




