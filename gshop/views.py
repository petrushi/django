from django.shortcuts import render
from mainapp.models import Product
from basketapp.models import Basket


def index(request, pk=None):
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
        
    title = 'gshop'
    products = Product.objects.all()[:4]

    context = {
        'products': products,
        'title': title,
        'basket': basket,

    }

    return render(request, 'index.html', context=context)


def contacts(request):
    return render(request, 'contact.html')
