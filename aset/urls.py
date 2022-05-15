from asyncore import read
from django.urls import path

from . import views

app_name = 'aset'

urlpatterns = [
    path('', views.index, name='pilihan-buat-aset'),
    path('list-aset/', views.list_aset, name='list-aset'),
    path('beli-aset/', views.form_beli_aset, name='beli-aset'),
    path('list-transaksi-beli-aset/', views.list_transaksi_pembelian_aset, name='list-transaksi-beli-aset'),
    path('list-koleksi-aset/', views.list_koleksi_aset, name='list-koleksi-aset'),
    path('form-bibit/', views.form_bibit_tanaman, name='form-bibit'),
    path('form-dekorasi/', views.form_dekorasi, name='form-dekorasi'),
    path('form-kandang/', views.form_kandang, name='form-kandang'),
    path('form-hewan/', views.form_hewan, name='form-hewan'),
    path('form-alat-produksi/', views.form_alat_produksi, name='form-alat-produksi'),
    path('form-petak-sawah/', views.form_petak_sawah, name='form-petak-sawah'),
    path('list-aset/list-dekorasi/', views.list_dekorasi, name='list-dekorasi'),
    path('list-aset/list-bibit-tanaman/', views.list_bibit_tanaman, name='list-bibit-tanaman'),
    path('list-aset/list-kandang/', views.list_kandang, name='list-kandang'),
    path('list-aset/list-hewan/', views.list_hewan, name='list-hewan'),
    path('list-aset/list-alat-produksi/', views.list_alat_produksi, name='list-alat'),
    path('list-aset/list-petak-sawah/', views.list_petak_sawah, name='list-petik-sawah')
    
]