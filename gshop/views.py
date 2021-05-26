from django.shortcuts import render

def index(request):
    return render(request, 'gshop/index.html')

def contacts(request):
    return render(request, 'gshop/contact.html')
