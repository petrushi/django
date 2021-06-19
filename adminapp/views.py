from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory

from adminapp.forms import ShopUserRegisterForm, CategoryEditForm, ProductEditForm

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    title = 'админка/пользователи'

    users_list = ShopUser.objects.filter(is_delete=False).order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    context = {
        'title': title,
        'objects': users_list
    }

    return render(request, 'adminapp/users.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    title = 'создание пользователя'

    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()

            return HttpResponseRedirect(reverse('admin_staff:users'))
    else:
        user_form = ShopUserRegisterForm()
    
    context = {
        'title': title,
        'update_form': user_form,
    }

    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    title = 'редактирование пользователя'

    edit_user = get_object_or_404(ShopUser, pk=pk)


    if request.method == 'POST':
        edit_form = ShopUserRegisterForm(request.POST, request.FILES, instance=edit_user)

        if edit_form.is_valid():
            edit_form.save()

            return HttpResponseRedirect(reverse('admin_staff:user_update', args=[edit_user.pk]))
    else:
        edit_form = ShopUserRegisterForm(instance=edit_user)
    
    context = {
        'title': title,
        'update_form': edit_form,
    }

    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    title = 'удаление пользователя'

    user = get_object_or_404(ShopUser, pk=pk)


    if request.method == 'POST':
        user.is_delete = True
        user.save()

        return HttpResponseRedirect(reverse('admin_staff:users'))

    context = {
        'title': title,
        'user_to_delete': user,
    }

    return render(request, 'adminapp/user_delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    title = 'админка/категории'

    categories_list = ProductCategory.objects.all()

    context = {
        'title': title,
        'objects': categories_list
    }

    return render(request, 'adminapp/categories.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    title = 'создание категории'

    if request.method == 'POST':
        category_form = CategoryEditForm(request.POST, request.FILES)
        if category_form.is_valid():
            category_form.save()

            return HttpResponseRedirect(reverse('admin_staff:categories'))
    else:
        category_form = CategoryEditForm()
    
    context = {
        'title': title,
        'update_form': category_form,
    }

    return render(request, 'adminapp/category_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    title = 'редактирование категории'

    edit_category = get_object_or_404(ProductCategory, pk=pk)


    if request.method == 'POST':
        edit_form = CategoryEditForm(request.POST, request.FILES, instance=edit_category)

        if edit_form.is_valid():
            edit_form.save()

            return HttpResponseRedirect(reverse('admin_staff:category_update', args=[edit_category.pk]))

    else:
        edit_form = CategoryEditForm(instance=edit_category)
    
    context = {
        'title': title,
        'update_form': edit_form,
    }

    return render(request, 'adminapp/category_update.html', context)

@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    title = 'удаление категории'

    category = get_object_or_404(ProductCategory, pk=pk)


    if request.method == 'POST':
        category.is_delete = True
        category.save()

        return HttpResponseRedirect(reverse('admin_staff:categories'))

    context = {
        'title': title,
        'category_to_delete': category,
    }

    return render(request, 'adminapp/category_delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk=None, page=1):
    title = 'админка/продукт'
    categories = ProductCategory.objects.all()

    if pk == 0:
        products = Product.objects.all()
        context = {
            'title': title,
            'objects': products,
            'categories': categories,
        }

        return render(request, 'adminapp/products.html', context)

    category = get_object_or_404(ProductCategory, pk=pk)
    products = Product.objects.filter(category__pk=pk)

    context = {
        'title': title,
        'category': category,
        'objects': products,
        'categories': categories,
    }

    return render(request, 'adminapp/products.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):

    title = 'создание продукта'
    product_category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()

            return HttpResponseRedirect(reverse('admin_staff:products', args=[pk]))
    else:
        product_form = ProductEditForm(initial={'category': product_category})

    context = {
        'title': title,
        'update_form': product_form,
        'category': product_category
    }

    return render(request, 'adminapp/product_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_read(request, pk):

    product = get_object_or_404(Product, pk=pk)
    title = f'продукты/{product.name}'

    context = {
        'title': title,
        'product': product,
    }

    return render(request, 'adminapp/product_read.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    title = 'редактирование продукта'

    edit_product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)
        if product_form.is_valid():
            product_form.save()

            return HttpResponseRedirect(reverse('admin_staff:product_update', args=[edit_product.pk]))
    else:
        product_form = ProductEditForm(instance=edit_product)

    context = {
        'title': title,
        'update_form': product_form,
    }

    return render(request, 'adminapp/product_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    title = 'удаление продукта'

    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.is_delete = True
        product.save()

        return HttpResponseRedirect(reverse('admin_staff:products', args=[product.category.pk]))

    context = {
        'title': title,
        'product_to_delete': product,
    }

    return render(request, 'adminapp/product_delete.html', context)
