from django.shortcuts import render, get_object_or_404
from django.views import View
from django.core.paginator import Paginator
from .models import Category, Product

class HomeView(View):
    def get(self, request):
        featured_products = Product.objects.filter(
            is_available=True
        ).select_related('category').prefetch_related('images')[:8]
        categories = Category.objects.filter(is_active=True)
        return render(request, 'home.html', {
            'featured_products': featured_products,
            'categories': categories,
        })


class ProductListView(View):

    def get(self, request):
        products = Product.objects.filter(is_available=True).select_related('category').prefetch_related('images')

        # Category filter
        category_slug = request.GET.get('category')
        selected_category = None
        if category_slug:
            selected_category = get_object_or_404(Category, slug=category_slug, is_active=True)
            products = products.filter(category=selected_category)

        # Search
        query = request.GET.get('q')
        if query:
            products = products.filter(name__icontains=query)

        # Sorting
        sort = request.GET.get('sort', 'name')
        sort_map = {
            'price_asc':  'price',
            'price_desc': '-price',
            'newest':     '-created_at',
            'name':       'name',
        }
        products = products.order_by(sort_map.get(sort, 'name'))

        # Pagination
        paginator = Paginator(products, 12)
        page = request.GET.get('page', 1)
        products = paginator.get_page(page)

        categories = Category.objects.filter(is_active=True)

        context = {
            'products': products,
            'categories': categories,
            'selected_category': selected_category,
            'query': query or '',
            'sort': sort,
        }
        return render(request, 'products/product_list.html', context)


class ProductDetailView(View):

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug, is_available=True)
        images = product.images.all()
        primary_image = images.filter(is_primary=True).first() or images.first()

        related_products = Product.objects.filter(
            category=product.category,
            is_available=True
        ).exclude(pk=product.pk)[:4]

        context = {
            'product': product,
            'images': images,
            'primary_image': primary_image,
            'related_products': related_products,
        }
        return render(request, 'products/product_detail.html', context)
