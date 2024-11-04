# store/context_processors.py

from .models import Category
from order.models import CartItem


def categories(request):
    """Return all categories to be used in templates."""
    return {
        'categories': Category.objects.all(),
        'cart_count': CartItem.objects.count() - 1,
    }
