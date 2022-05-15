from asyncore import read
from django.urls import path

from . import views

app_name = 'lumbung'

urlpatterns = [
    path('', views.list_lumbung, name='list_lumbung'),
    path('list-transaksi', views.list_transaksi_upgrade_lumbung, name='list_transaksi'),
    path('transaksi-upgrade-lumbung', views.transaksi_upgrade_lumbung, name='transaksi_upgrade_lumbung'),
    path('histori-tanaman', views.histori_tanaman, name='histori_tanaman'),
    path('list-histori-tanaman', views.list_histori_tanaman, name='list_histori_tanaman')
]
