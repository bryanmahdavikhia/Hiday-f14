
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
    cursor = connection.cursor()
    cursor.execute("SET search_path TO hidayf14")
    cursor.execute("SELECT nama FROM aset, bibit_tanaman WHERE id=id_aset;")
    data = cursor.fetchall()
    return render(request, 'form_kandang.html',{"data":data})

def form_hewan(request):
    return render(request, 'form_hewan.html')

def form_alat_produksi(request):
    return render(request, 'form_alat_produksi.html')

def form_petak_sawah(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO hidayf14")
    cursor.execute("SELECT nama FROM aset, bibit_tanaman WHERE id=id_aset;")
    data = cursor.fetchall()
    return render(request, 'form_petak_sawah.html',{"data":data})

def form_beli_aset(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO hidayf14") #harus dicek lagi

    list_aset = "SELECT nama, harga_beli FROM aset;"
    cursor.execute(list_aset)
    data = cursor.fetchall()
    return render(request, 'form_beli_aset.html',{"dropDownAset":data})

def list_transaksi_pembelian_aset(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO hidayf14") 

    list_aset = "SELECT email, waktu, nama, jumlah, jumlah*harga_beli AS total_harga FROM aset,transaksi_pembelian WHERE id=id_aset;"
    cursor.execute(list_aset)
    data = cursor.fetchall()
    return render(request, 'list_transaksi_beli_aset.html',{"data":data})

def list_aset(request):
    return render(request, 'list_aset.html')

def list_koleksi_aset(request):
    
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")

    if request.session.has_key('account'):
        role = request.session['role']
        if role == "admin":
            cursor.execute("SET search_path TO hidayf14") 

            list_aset = "SELECT id_koleksi_aset, nama, minimum_level, harga_beli, jumlah FROM aset, koleksi_aset_memiliki_aset WHERE id=id_aset;"
            cursor.execute(list_aset)
            data = cursor.fetchall()
            return render(request, 'list_koleksi_aset.html',{"data":data})
        elif role == "pengguna":
            cursor.execute("SET search_path TO hidayf14") 

            list_aset = "SELECT nama, minimum_level, harga_beli, jumlah FROM aset, koleksi_aset_memiliki_aset WHERE id=id_aset;"
            cursor.execute(list_aset)
            data = cursor.fetchall()
            return render(request, 'list_koleksi_aset.html',{"data":data})
        

def list_dekorasi(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")

    if request.session.has_key('account'):
        if request.session['role'] == "admin":
            role = "admin"
        else:
            role = None

    cursor.execute("SET search_path TO hidayf14")
    query = "SELECT id, nama, minimum_level, harga_beli, harga_jual FROM aset, dekorasi WHERE id=id_aset;"
    cursor.execute(query)
    data = cursor.fetchall()
    return render(request, 'list_dekorasi.html', {'data': data, 'role': role})

def list_bibit_tanaman(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('account'):
        if request.session['role'] == "admin":
            role = "admin"
        else:
            role = None

    cursor.execute("SET search_path TO hidayf14")
    query = "SELECT id, nama, minimum_level, harga_beli, durasi_panen FROM aset, bibit_tanaman WHERE id=id_aset;"
    cursor.execute(query)
    data = cursor.fetchall()
    return render(request, 'list_bibit_tanaman.html', {'data': data,'role': role})

def list_kandang(request):
    cursor = connection.cursor()
    
    cursor.execute("SET search_path TO public")
    if request.session.has_key('account'):
        if request.session['role'] == "admin":
            role = "admin"
        else:
            role = None

    cursor.execute("SET search_path TO hidayf14")
    query = "SELECT id, nama, minimum_level, harga_beli, kapasitas_maks, jenis_hewan FROM aset, kandang WHERE id=id_aset;"
    cursor.execute(query)
    data = cursor.fetchall()
    return render(request, 'list_kandang.html', {'data': data,'role': role})

def list_hewan(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('account'):
        if request.session['role'] == "admin":
            role = "admin"
        else:
            role = None

    cursor.execute("SET search_path TO hidayf14")
    query = "SELECT a.id, a.nama, a.minimum_level, a.harga_beli, h.durasi_produksi, h.id_kandang FROM aset AS a, hewan AS h, kandang as k WHERE A.id=H.id_aset AND k.id_aset = h.id_kandang;"
    cursor.execute(query)
    data = cursor.fetchall()
    return render(request, 'list_hewan.html', {'data': data,'role': role})

def list_alat_produksi(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('account'):
        if request.session['role'] == "admin":
            role = "admin"
        else:
            role = None

    cursor.execute("SET search_path TO hidayf14")
    query = "SELECT id, nama, minimum_level, harga_beli, kapasitas_maks FROM aset, alat_produksi WHERE id=id_aset;"
    cursor.execute(query)
    data = cursor.fetchall()
    return render(request, 'list_alat_produksi.html', {'data': data,'role': role})

def list_petak_sawah(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('account'):
        if request.session['role'] == "admin":
            role = "admin"
        else:
            role = None

    cursor.execute("SET search_path TO hidayf14")
    query = "SELECT id, nama, minimum_level, harga_beli, jenis_tanaman FROM aset, petak_sawah WHERE id=id_aset;"
    cursor.execute(query)
    data = cursor.fetchall()
    return render(request, 'list_petak_sawah.html', {'data': data,'role': role})
    