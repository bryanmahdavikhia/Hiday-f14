from hashlib import new
import re
from django.db import connection
from collections import namedtuple
from django.shortcuts import redirect, render
from django.contrib import messages

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
        cursor.execute("SELECT * FROM LUMBUNG WHERE email = %s", [request.session['account'][0]])
        data_lumbung = cursor.fetchone()
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
            
            cursor.execute("SELECT koin FROM pengguna WHERE email = '"+ request.session['account'][0] + "'")
            koin = cursor.fetchall()
            coin = koin[0][0]
            print(coin)
            
            
            if request.method == "POST":
                if coin < 200:
                    messages.warning(request, "Koin anda tidak cukup, silahkan cari Koin terlebih dahulu.")
                else:
                    cursor.execute("select (now() + interval '7 hours')::timestamp")
                    timestamp = cursor.fetchall()
                    time_str = str(timestamp[0][0])
                    
                    cursor.execute("INSERT into transaksi_upgrade_lumbung VALUES ('"+request.session['account'][0]+"', '"+time_str + "'::timestamp)")
                    cursor.execute("UPDATE lumbung SET level = %s, kapasitas_maksimal = %s where email = %s", [level_upgrade, kapasitas_upgrade, request.session['account'][0]])
                    
                    return redirect('lumbung:list_transaksi')
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
            cursor.execute("SELECT bt.id_aset FROM bibit_tanaman bt, koleksi_aset_memiliki_aset ka WHERE bt.id_aset = ka.id_aset and ka.id_koleksi_aset = %s", [request.session['account'][0]])
            data = cursor.fetchall()
            print(data)
            if request.method == "POST":
                bibit = request.POST["bibit"]
                jumlah = int(request.POST["jumlah"])
                # xp = request.POST["xp"]
                xp = 5
                
                cursor.execute("select jumlah from koleksi_aset_memiliki_aset where id_aset = %s and id_koleksi_aset = %s", [bibit, request.session['account'][0]])
                banyak = cursor.fetchall()
                if jumlah > banyak[0][0]:
                    messages.warning(request, "Anda tidak memiliki bibit yang cukup, silahkan membeli bibit terlebih dahulu")
                else:
                    xp_dapat = xp*jumlah
                    cursor.execute("select (now() + interval '7 hours')::timestamp")
                    timestamp = cursor.fetchall()
                    time_str = str(timestamp[0][0])
                    
                    cursor.execute("insert into histori_produksi values ('"+request.session['account'][0]+"', '"+time_str + "'::timestamp, '"+time_str + "'::timestamp, '"+str(jumlah)+"', '"+str(xp_dapat)+"')")
                    cursor.execute("insert into histori_tanaman values ('"+request.session['account'][0]+"', '"+time_str + "'::timestamp, '"+str(bibit)+"')")
                    return redirect("lumbung:list_histori_tanaman")
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

    
