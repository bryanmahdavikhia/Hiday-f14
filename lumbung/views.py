from hashlib import new
import re
from django.db import connection
from collections import namedtuple
from django.shortcuts import redirect, render

# Create your views here.

def list_lumbung(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
                
    if request.session.has_key('account'):
        if request.session['role'] == "admin":
            role = "admin"
        else:
            role = None
            
    cursor.execute("SET search_path TO hidayf14")
 
    if role == 'admin': 
        
        # Produk Hasil Panen
        hasil_panen = object_entitas('select email, id, nama, harga_jual, sifat_produk, jumlah from lumbung l, lumbung_memiliki_produk lmp, produk p where l.email = lmp.id_lumbung and lmp.id_produk = p.id and p.id in (select * from hasil_panen)')
        # Produk Hewan
        hewan = object_entitas('select email, id, nama, harga_jual, sifat_produk, jumlah from lumbung l, lumbung_memiliki_produk lmp, produk p where l.email = lmp.id_lumbung and lmp.id_produk = p.id and p.id in (select * from produk_hewan)')
        # Produk Makanan
        makanan = object_entitas('select email, id, nama, harga_jual, sifat_produk, jumlah from lumbung l, lumbung_memiliki_produk lmp, produk p where l.email = lmp.id_lumbung and lmp.id_produk = p.id and p.id in (select * from produk_makanan)')
        
        cursor.execute("SET search_path TO public")
        return render(request, 'list_lumbung.html', {'role': role, 'hasil_panen': hasil_panen, 'hewan': hewan, 'makanan': makanan })
    else:
        
        # Produk Hasil Panen
        hasil_panen = object_entitas("select email, id, nama, harga_jual, sifat_produk, jumlah from lumbung l, lumbung_memiliki_produk lmp, produk p where l.email = lmp.id_lumbung and lmp.id_produk = p.id and l.email = '"+ request.session['account'][0] +"' and p.id in (select * from hasil_panen)")
        # Produk Hewan
        hewan = object_entitas("select email, id, nama, harga_jual, sifat_produk, jumlah from lumbung l, lumbung_memiliki_produk lmp, produk p where l.email = lmp.id_lumbung and lmp.id_produk = p.id and l.email = '"+ request.session['account'][0] +"' and p.id in (select * from produk_hewan)")
        # Produk Makanan
        makanan = object_entitas("select email, id, nama, harga_jual, sifat_produk, jumlah from lumbung l, lumbung_memiliki_produk lmp, produk p where l.email = lmp.id_lumbung and lmp.id_produk = p.id and l.email = '"+ request.session['account'][0] +"' and p.id in (select * from produk_makanan)")
        
        cursor.execute("select * from hidayf14.lumbung l where l.email = '"+ request.session['account'][0] +"'")
        pengguna = cursor.fetchall()
        
        cursor.execute("SET search_path TO public")
        return render(request, 'list_lumbung.html', {'role': role, 'hasil_panen': hasil_panen, 'hewan': hewan, 'makanan': makanan, 'pengguna': pengguna })
        
def object_entitas(query): # mengembalikan value relasi dalam bentuk object (class) dalam bentuk list
     # source code: https://dev.to/stndaru/connecting-django-to-postgresql-on-heroku-and-perform-sql-command-4m8e
    cursor = connection.cursor()
    cursor.execute("SET search_path TO hidayf14")
    result = []
    cursor.execute(query)

    desc = cursor.description
    nt_result = namedtuple('Hasil_Panen', [col[0] for col in desc])
    result = [nt_result(*row) for row in cursor.fetchall()]
    number_result = {}
    cursor.execute('SET search_path TO public')

    sum_of_entitites = range(len(result)-1)
    for i in sum_of_entitites:
        number_result[i+1] = result[i]
    
    return list(number_result.items())

def list_transaksi_upgrade_lumbung(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
                
    if request.session.has_key('account'):
        if request.session['role'] == "admin":
            role = "admin"
        else:
            role = None
    
    cursor.execute("SET search_path TO hidayf14")
    if role == "admin":
        cursor.execute("SELECT * FROM transaksi_upgrade_lumbung")
        data = cursor.fetchall()
    else:
        cursor.execute("SELECT * FROM transaksi_upgrade_lumbung WHERE email = '" + request.session['account'][0] + "'")
        data = cursor.fetchall()
        
    return render(request, 'list_transaksi_upgrade_lumbung.html', {'data': data, 'role': role})

def transaksi_upgrade_lumbung(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    
    if request.session.has_key('account'):
        role = request.session['role']
        if request.session['role'] == "admin":
            role = "admin"
        else:
            role = None
            
        if role == None:
            cursor.execute("SET search_path TO hidayf14")
            cursor.execute("SELECT * FROM lumbung l WHERE l.email = '" + request.session['account'][0] + "'")
            data = cursor.fetchall()
            level = data[0][1]
            kapasitas = data[0][2]
            level_upgrade = level+1
            kapasitas_upgrade = kapasitas+50
            print(level)
            
    return render(request, 'transaksi_upgrade_lumbung.html', {'data':data, 'role': role, 'level':level_upgrade, 'kapasitas':kapasitas_upgrade})
 
def histori_tanaman(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    
    if request.session.has_key('account'):
        role = request.session['role']
        if request.session['role'] == "admin":
            role = "admin"
        else:
            role = None
            
        if role == None:
            cursor.execute("SET search_path TO hidayf14")
            cursor.execute("SELECT id_aset FROM bibit_tanaman")
            data = cursor.fetchall()
            
    return render(request, 'histori_tanaman.html', {'data':data, 'role': role})

def list_histori_tanaman(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    
    if request.session.has_key('account'):
        role = request.session['role']
        if request.session['role'] == "admin":
            role = "admin"
        else:
            role = None
    
    cursor.execute("SET search_path TO hidayf14")
    if role == "admin":
        cursor.execute("select hp.email, hp.waktu_awal, hp.waktu_selesai, hp.jumlah, hp.xp, a.nama from histori_produksi hp JOIN histori_tanaman ht on hp.email = ht.email and hp.waktu_awal = ht.waktu_awal JOIN bibit_tanaman bt on ht.id_bibit_tanaman = bt.id_aset JOIN aset a on bt.id_aset = a.id")
        data = cursor.fetchall()
    else:
        cursor.execute("select hp.email, hp.waktu_awal, hp.waktu_selesai, hp.jumlah, hp.xp, a.nama from histori_produksi hp JOIN histori_tanaman ht on hp.email = ht.email and hp.waktu_awal = ht.waktu_awal JOIN bibit_tanaman bt on ht.id_bibit_tanaman = bt.id_aset JOIN aset a on bt.id_aset = a.id WHERE hp.email = '" + request.session['account'][0] + "'")
        data = cursor.fetchall()
        
    return render(request, 'list_histori_tanaman.html', {'data': data, 'role': role})

    
