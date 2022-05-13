from hashlib import new
import re
from django.db import connection
from django.shortcuts import redirect, render

# Create your views here.
def create_product(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")

    if request.session.has_key('account'):
        role = request.session['role']
        if role == "admin":
            if request.method == "POST":
                product_type = request.POST["type"]
                name = request.POST["name"]
                price = request.POST["price"]
                characteristic = request.POST["characteristic"]

                cursor.execute("SET search_path TO hidayf14")
                cursor.execute("SELECT nama FROM produk WHERE nama like %s", [name])
                if cursor.fetchone() is not None:
                    return redirect("produk:create_product")

                if product_type == "hasil panen":
                    cursor.execute("SELECT id_produk FROM hasil_panen ORDER BY ascii(id_produk) DESC LIMIT 1")
                    id = cursor.fetchone()
                    if id is None:
                        id = "HP001"
                    else:
                        id = str(id)
                        id = "HP" + str(int(id[4:7]) + 1).zfill(3)
                    cursor.execute("INSERT INTO produk VALUES (%s, %s, %s, %s)", [id, name, price, characteristic])
                    cursor.execute("INSERT INTO hasil_panen VALUES (%s)", [id])

                elif product_type == "produk hewan":
                    cursor.execute("SELECT id_produk FROM produk_hewan ORDER BY ascii(id_produk) DESC LIMIT 1")
                    id = cursor.fetchone()
                    if id is None:
                        id = "PH001"
                    else:
                        id = str(id)
                        id = "PH" + str(int(id[4:7]) + 1).zfill(3)
                    cursor.execute("INSERT INTO produk VALUES (%s, %s, %s, %s)", [id, name, price, characteristic])
                    cursor.execute("INSERT INTO produk_hewan VALUES (%s)", [id])

                else:
                    cursor.execute("SELECT id_produk FROM produk_makanan ORDER BY ascii(id_produk) DESC LIMIT 1")
                    id = cursor.fetchone()
                    if id is None:
                        id = "PM001"
                    else:
                        id = str(id)
                        id = "PM" + str(int(id[4:7]) + 1).zfill(3)
                    cursor.execute("INSERT INTO produk VALUES (%s, %s, %s, %s)", [id, name, price, characteristic])
                    cursor.execute("INSERT INTO produk_makanan VALUES (%s)", [id])
                return redirect("product:list_product")
            
            else:
                return render(request, "form_produk.html", {})
            
        else:
            return redirect("product:list_product")
    else:
        return redirect("home:login")

def list_product(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")

    if request.session.has_key('account'):
        if request.session['role'] == "admin":
            role = "admin"
        else:
            role = None
        
        cursor.execute("SET search_path TO hidayf14")
        cursor.execute("SELECT * FROM produk")
        data = cursor.fetchall()
        return render(request, 'list_produk.html', {'data': data, 'role': role})

def update_product(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")

    if request.session.has_key('account'):
        role = request.session['role']
        if role == "admin":
            if request.method == "POST":
                # product_type = request.POST["type"]
                # name = request.POST["name"]
                # price = request.POST["price"]
                # characteristic = request.POST["characteristic"]
                return redirect("product:list_product")
            else:
                return render(request, 'update_produk.html', {})
        else:
            return redirect("product:list_product")
    else:
        return redirect("home:login")

def create_production(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")

    if request.session.has_key('account'):
        role = request.session['role']
        if role == "admin":
            if request.method == "POST":
                # product_type = request.POST["type"]
                # name = request.POST["name"]
                # price = request.POST["price"]
                # characteristic = request.POST["characteristic"]
                print(request.POST.getlist("jumlah[]"))
                return redirect("product:list_product")
            else:
                return render(request, 'form_produksi.html', {})
        else:
            return redirect("product:list_product")
    else:
        return redirect("home:login")

def list_production(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")

    if request.session.has_key('account'):
        if request.session['role'] == "admin":
            role = "admin"
        else:
            role = None
        cursor.execute("SET search_path TO hidayf14") #buat indexing ntar
        query = "SELECT pr.nama, a.nama, x.durasi, x.jumlah_unit_hasil "
        query += "FROM (SELECT * FROM produksi p, alat_produksi ap, produk_makanan pm "
        query += "WHERE p.id_alat_produksi = ap.id_aset and p.id_produk_makanan = pm.id_produk) "
        query += "x LEFT OUTER JOIN aset a ON x.id_alat_produksi = a.id LEFT OUTER JOIN produk pr ON x.id_produk_makanan = pr.id"
        cursor.execute(query)
        data = cursor.fetchall()
        return render(request, 'list_produksi.html', {'data': data, 'role': role})

def detail_production(request, id):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")

    if request.session.has_key('account'):
        cursor.execute("SET search_path TO hidayf14")
        query = "SELECT pr.nama, a.nama, x.durasi, x.jumlah_unit_hasil, x.id_produk_makanan "
        query += "FROM (SELECT * FROM produksi p, alat_produksi ap, produk_makanan pm "
        query += "WHERE p.id_alat_produksi = ap.id_aset and p.id_produk_makanan = pm.id_produk) "
        query += "x LEFT OUTER JOIN aset a ON x.id_alat_produksi = a.id LEFT OUTER JOIN produk pr ON x.id_produk_makanan = pr.id"
        cursor.execute(query)
        data = cursor.fetchall()
        selected_data = data[id-1]
        new_query = "SELECT p.nama, pd.jumlah "
        new_query += "FROM produk_dibutuhkan_oleh_produk_makanan pd LEFT OUTER JOIN produk p "
        new_query += "ON pd.id_produk = p.id "
        str = "WHERE pd.id_produk_makanan LIKE '%s'" % selected_data[4]
        new_query += str
        cursor.execute(new_query)
        detail_data = cursor.fetchall()
        return render(request, 'detail_produksi.html', {'produksi': selected_data, 'bahan': detail_data})

def update_production(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")

    if request.session.has_key('account'):
        role = request.session['role']
        if role == "admin":
            if request.method == "POST":
                return redirect("product:list_production")
            else:
                return render(request, 'update_produksi.html', {})
        else:
            return redirect("product:list_production")
    else:
        return redirect("home:login")

def create_product_history(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")

    if request.session.has_key('account'):
        role = request.session['role']
        if role == "pengguna":
            if request.method == "POST":
                return redirect("product:list_product")
            else:
                return render(request, 'form_histori_produk.html', {})
        else:
            return redirect("product:list_product")
    else:
        return redirect("home:login")

def list_product_history(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")

    if request.session.has_key('account'):
        if request.session['role'] == "admin":
            role = "admin"
        else:
            role = None
        email = request.session['account']
        cursor.execute("SET search_path TO hidayf14") #buat indexing ntar yang sama kek detail production
        query = "SELECT hpm.email, hpm.waktu_awal::time, hp.waktu_selesai::time, hp.jumlah, hp.xp, pr.nama, a.nama "
        query += "FROM histori_produksi_makanan hpm LEFT OUTER JOIN histori_produksi hp "
        query += "ON (hpm.email = hp.email AND hpm.waktu_awal = hp.waktu_awal)"
        query += "LEFT OUTER JOIN (SELECT * FROM produksi p, alat_produksi ap, produk_makanan pm "
        query += "WHERE p.id_alat_produksi = ap.id_aset and p.id_produk_makanan = pm.id_produk) "
        query += "x ON (hpm.id_alat_produksi = x.id_alat_produksi AND hpm.id_produk_makanan = x.id_produk_makanan) "
        query += "LEFT OUTER JOIN aset a ON x.id_alat_produksi = a.id LEFT OUTER JOIN produk pr ON x.id_produk_makanan = pr.id"
        if role == None:
            str = " WHERE hpm.email LIKE '%s'" % email[0]
            query += str
        cursor.execute(query)
        detail_data = cursor.fetchall()
        return render(request, 'list_histori.html', {'data': detail_data, 'role': role})