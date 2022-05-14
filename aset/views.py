
from hashlib import new
from django.db import connection
from django.shortcuts import redirect, render


def index(request):
    return render(request, 'createAsset.html')

def form_bibit_tanaman(request):
    return render(request, 'form_bibit_tanaman.html')

def form_dekorasi(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    return render(request, 'form_dekorasi.html')

def form_kandang(request):
    return render(request, 'form_kandang.html')

def form_hewan(request):
    return render(request, 'form_hewan.html')

def form_alat_produksi(request):
    return render(request, 'form_alat_produksi.html')

def form_petak_sawah(request):
    return render(request, 'form_petak_sawah.html')

def list_aset(request):
    return render(request, 'list_aset.html')

def list_dekorasi(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")

    cursor.execute("SET search_path TO hidayf14")
    query = "SELECT id, nama, minimum_level, harga_beli, harga_jual FROM aset, dekorasi WHERE id=id_aset;"
    cursor.execute(query)
    data = cursor.fetchall()
    return render(request, 'list_dekorasi.html', {'data': data})

def list_bibit_tanaman(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")

    cursor.execute("SET search_path TO hidayf14")
    query = "SELECT id, nama, minimum_level, harga_beli, durasi_panen FROM aset, bibit_tanaman WHERE id=id_aset;"
    cursor.execute(query)
    data = cursor.fetchall()
    return render(request, 'list_bibit_tanaman.html', {'data': data})

def list_kandang(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")

    cursor.execute("SET search_path TO hidayf14")
    query = "SELECT id, nama, minimum_level, harga_beli, kapasitas_maks, jenis_hewan FROM aset, kandang WHERE id=id_aset;"
    cursor.execute(query)
    data = cursor.fetchall()
    return render(request, 'list_kandang.html', {'data': data})

def list_hewan(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")

    cursor.execute("SET search_path TO hidayf14")
    query = "SELECT a.id, a.nama, a.minimum_level, a.harga_beli, h.durasi_produksi, h.id_kandang FROM aset AS a, hewan AS h, kandang as k WHERE A.id=H.id_aset AND k.id_aset = h.id_kandang;"
    cursor.execute(query)
    data = cursor.fetchall()
    return render(request, 'list_hewan.html', {'data': data})

def list_alat_produksi(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")

    cursor.execute("SET search_path TO hidayf14")
    query = "SELECT id, nama, minimum_level, harga_beli, kapasitas_maks FROM aset, alat_produksi WHERE id=id_aset;"
    cursor.execute(query)
    data = cursor.fetchall()
    return render(request, 'list_alat_produksi.html', {'data': data})

def list_petak_sawah(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")

    cursor.execute("SET search_path TO hidayf14")
    query = "SELECT id, nama, minimum_level, harga_beli, jenis_tanaman FROM aset, petak_sawah WHERE id=id_aset;"
    cursor.execute(query)
    data = cursor.fetchall()
    return render(request, 'list_petak_sawah.html', {'data': data})
    