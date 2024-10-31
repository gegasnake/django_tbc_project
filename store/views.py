from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView
from store.models import Category, Product, Tag
from django.contrib.auth.decorators import login_required


@method_decorator(login_required, name='dispatch')
class HomePageView(TemplateView):
    template_name = 'index.html'


@method_decorator(login_required, name='dispatch')
class ProductDetailView(TemplateView):
    template_name = 'shop-detail.html'


class ContactView(TemplateView):
    template_name = 'contact.html'


@method_decorator(login_required, name='dispatch')
class ProductListView(ListView):
    template_name = 'shop.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Start with the base queryset
        queryset = Product.objects.select_related('category').prefetch_related('tags')

        # Category filter
        category_slug = self.kwargs.get('slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)

        # Search query filter
        query = self.request.GET.get('search_bar')
        if query:
            queryset = queryset.filter(name__icontains=query)

        # Tag filter
        tag = self.request.GET.get('tag')
        if tag:
            queryset = queryset.filter(tags__name=tag)

        # Price filter
        price = self.request.GET.get('rangeInput')
        if price:
            try:
                price = float(price)
                queryset = queryset.filter(price__lte=price)
            except ValueError:
                pass

        # Sorting
        sort = self.request.GET.get('sort', '')
        if sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')
        elif sort == 'newest':
            queryset = queryset.order_by('created_at')
        else:
            queryset = queryset.order_by('name')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch data for context
        tags = Tag.objects.all()
        root_categories = Category.objects.filter(parent=None)
        category_slug = self.kwargs.get('slug')
        category = get_object_or_404(Category, slug=category_slug) if category_slug else None

        # Pagination
        paginator = Paginator(self.get_queryset(), 6)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Update context
        context.update({
            'tags': tags,
            'categories': root_categories,
            'category': category,
            'child_categories': category.children.all() if category else None,
            'page_obj': page_obj,
        })

        return context
