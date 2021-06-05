from django.shortcuts import render, get_object_or_404
from .models import Product, ProductCategory


def products(request, pk=None):
    title = 'Каталог/Продукты'
    links_menu = ProductCategory.objects.all()

    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category = {'name': 'все'}
        else:
            products = Product.objects.filter(category__pk=pk).order_by('price')
            category = get_object_or_404(ProductCategory, pk=pk)

        context = {
            'products': products,
            'title': title,
            'category': category,
            'links_menu': links_menu
        }

        return render(request, 'mainapp/product.html', context=context)

    products = Product.objects.all()
    context = {
        'links_menu': links_menu,
        'title': title,
        'products': products,
    }
    return render(request, 'mainapp/products.html', context=context)
