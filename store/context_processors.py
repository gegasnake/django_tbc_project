# store/context_processors.py

from .models import Category


def categories(request):
    """Return all categories to be used in templates."""
    return {
        'categories': Category.objects.all(),
    }
