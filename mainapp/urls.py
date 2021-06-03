from django.urls import path
from  .views import products

app_name = 'mainapp'

urlpatterns = [
    path('', products, name='products'),
    path('product/<int:pk>/', products, name='index')

]
