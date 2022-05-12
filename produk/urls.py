from asyncore import read
from django.urls import path

from . import views

app_name = 'produk'

urlpatterns = [
    path('create-product', views.create_product, name='create_product'),
    path('', views.read_product, name='list_product'),
    path('update-product', views.update_product, name='update_product')
]