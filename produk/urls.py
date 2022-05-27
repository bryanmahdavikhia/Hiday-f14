from asyncore import read
from django.urls import path

from . import views

app_name = 'product'

urlpatterns = [
    path('create-product', views.create_product, name='create_product'),
    path('', views.list_product, name='list_product'),
    path('update-product/<str:id>', views.update_product, name='update_product'),
    path('delete-product/<str:id>', views.delete_product, name='delete_product'),
    path('create-production', views.create_production, name='create_product'),
    path('list-production', views.list_production, name='list_production'),
    path('detail-production/<int:id>', views.detail_production, name='detail_production'),
    path('update-production/<int:id>', views.update_production, name='update_production'),
    path('delete-production/<int:id>', views.delete_production, name='delete_production'),
    path('create-history', views.create_product_history, name='create_product_history'),
    path('list-history', views.list_product_history, name='list_history')
]