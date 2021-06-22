from basketapp.models import Basket
from django.shortcuts import render, get_object_or_404
from .models import Product, ProductCategory
import random

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []


def get_hot_product():
    hot_products = Product.objects.all()

    return random.sample(list(hot_products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(
        category=hot_product.category).exclude(pk=hot_product.pk)[:3]

    return same_products


def products(request, pk=None, page=1):
    title = 'Каталог/Продукты'
    links_menu = ProductCategory.objects.all()
    basket = []

    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    if pk is not None:
        if pk == 0:
            all_products = Product.objects.all().order_by('price')
            category = {
                'pk': 0,
                'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            all_products = Product.objects.filter(
                category__pk=pk).order_by('price')

        paginator = Paginator(all_products, 1)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = [paginator.page(paginator.num_pages)]

        context = {
            'products': products_paginator,
            'title': title,
            'category': category,
            'links_menu': links_menu,
            'basket': basket,
        }

        return render(request, 'mainapp/product.html', context=context)

    products = Product.objects.all()
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    paginator = Paginator(products, 1)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = [paginator.page(paginator.num_pages)]
    context = {
        'links_menu': links_menu,
        'title': title,
        'products': products_paginator,
        'basket': basket,
        'hot_product': hot_product,
        'same_products': same_products,
    }
    return render(request, 'mainapp/products.html', context=context)
