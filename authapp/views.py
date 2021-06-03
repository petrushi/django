from django.shortcuts import render


def login(request):
    title = 'страница входа'

    login_form = ShopUserLoginForm(data=request.POST)
