from asyncore import read
from django.urls import path

from . import views

app_name = 'paket_koin'

urlpatterns = [
    path('', views.list_paket, name='list_paket'),
    path('create-paket-koin', views.create_paket, name='create_paket'),
    path('update-paket-koin/<int:value>/<int:harga>', views.update_paket, name='update_paket'),
    path('list-transaksi', views.list_transaksi, name='list_transaksi'),
    path('beli-paket-koin/<int:value>/<int:harga>', views.beli_paket_koin, name='beli_paket_koin')

]