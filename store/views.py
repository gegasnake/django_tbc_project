from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView, ListView, FormView
from django_tbc_project.settings import EMAIL_HOST_USER
from store.forms import ContactForm
from store.models import Category, Product, Tag
from django.contrib.auth.decorators import login_required


@method_decorator([login_required, cache_page(600)], name='dispatch')
class HomePageView(TemplateView):
    template_name = 'index.html'


@method_decorator([login_required, cache_page(600)], name='dispatch')
class ProductDetailView(TemplateView):
    template_name = 'shop-detail.html'


@method_decorator([login_required, cache_page(600)], name='dispatch')
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


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)


def custom_500_view(request):
    return render(request, '500.html', status=500)


@method_decorator(cache_page(600), name='dispatch')
class ContactView(FormView):
    template_name = 'contact.html'  # Template to render
    form_class = ContactForm  # Form class to use
    success_url = '/'  # Redirect URL after successful submission

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']

        # Send email
        send_mail(
            subject=f'Contact Form Submission from {name}',
            message=message,
            from_email=email,
            recipient_list=['EMAIL_HOST_USER'],  # Replace with your recipient email
            fail_silently=False,
        )

        messages.success(self.request, 'Your message has been sent successfully!')
        return super().form_valid(form)  # Call the parent class's form_valid method
