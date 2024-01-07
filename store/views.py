from django.db.models import Count
from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def product_all(request):
    products = Product.products.all()
    product_count = products.count()
    product_category = Category.objects.annotate(num_products=Count('product'))

    return render(request, 'store/home.html', {
        'products': products,
        'product_count': product_count,
        'product_category': product_category
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    return render(request, 'store/products/detail.html', {'product': product})


def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/products/category.html', {'category': category, 'products': products})
