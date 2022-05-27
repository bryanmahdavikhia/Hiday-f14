from hashlib import new
from django.db import connection
from django.shortcuts import redirect, render
from django.contrib import messages
import datetime

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
                    cursor.execute("SELECT id_produk FROM hasil_panen ORDER BY id_produk DESC LIMIT 1")
                    id = cursor.fetchone()
                    if id is None:
                        id = "HP001"
                    else:
                        id = str(id)
                        id = "HP" + str(int(id[4:7]) + 1).zfill(3)
                    cursor.execute("INSERT INTO produk VALUES (%s, %s, %s, %s)", [id, name, price, characteristic])
                    cursor.execute("INSERT INTO hasil_panen VALUES (%s)", [id])

                elif product_type == "produk hewan":
                    cursor.execute("SELECT id_produk FROM produk_hewan ORDER BY id_produk DESC LIMIT 1")
                    id = cursor.fetchone()
                    if id is None:
                        id = "PH001"
                    else:
                        id = str(id)
                        id = "PH" + str(int(id[4:7]) + 1).zfill(3)
                    cursor.execute("INSERT INTO produk VALUES (%s, %s, %s, %s)", [id, name, price, characteristic])
                    cursor.execute("INSERT INTO produk_hewan VALUES (%s)", [id])

                else:
                    cursor.execute("SELECT id_produk FROM produk_makanan ORDER BY id_produk DESC LIMIT 1")
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
        query = "SELECT id, nama, harga_jual, sifat_produk, CASE "
        query += "WHEN exists(SELECT * FROM detail_pesanan WHERE id_produk = produk.id) "
        query += "OR exists(SELECT * FROM lumbung_memiliki_produk WHERE id_produk = produk.id) "
        query += "OR exists(SELECT * FROM produk_dibutuhkan_oleh_produk_makanan WHERE (id_produk = produk.id OR id_produk_makanan = produk.id)) "
        query += "OR exists(SELECT * FROM PRODUKSI WHERE id_produk_makanan = produk.id) "
        query += "OR exists(SELECT * FROM hewan_menghasilkan_produk_hewan WHERE id_produk_hewan = produk.id) "
        query += "OR exists(SELECT * FROM bibit_tanaman_menghasilkan_hasil_panen WHERE id_hasil_panen = produk.id) "
        query += "THEN false ELSE true END FROM produk"
        cursor.execute(query)
        data = cursor.fetchall()
        return render(request, 'list_produk.html', {'data': data, 'role': role})

def update_product(request, id):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")

    if request.session.has_key('account'):
        role = request.session['role']
        if role == "admin":
            if request.method == "POST":
                product_id = request.POST["id"]
                price = request.POST["price"]
                characteristic = request.POST["characteristic"]
                cursor.execute("SET search_path TO hidayf14")
                cursor.execute("UPDATE PRODUK SET harga_jual = %s, sifat_produk = %s WHERE id LIKE %s", [price, characteristic, product_id])
                return redirect("product:list_product")
            else:
                cursor.execute("SET search_path TO hidayf14")
                cursor.execute("SELECT * FROM produk WHERE id like %s", [id])
                data = cursor.fetchone()
                return render(request, 'update_produk.html', {'data': data})
        else:
            return redirect("product:list_product")
    else:
        return redirect("home:login")

def delete_product(request, id):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")

    if request.session.has_key('account'):
        role = request.session['role']
        if role == "admin":
            cursor.execute("SET search_path TO hidayf14")
            cursor.execute("DELETE FROM PRODUK WHERE id LIKE %s", [id])
            return redirect("product:list_product")
            
def create_production(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")

    if request.session.has_key('account'):
        role = request.session['role']
        if role == "admin":
            if request.method == "POST":
                food = request.POST["food"]
                tool = request.POST["tool"]
                duration = request.POST["duration"]
                duration = str(datetime.timedelta(seconds=(int(duration)*60)))
                amount = request.POST["amount"]
                ingredient_list = request.POST.getlist("bahan[]")
                amount_list = request.POST.getlist("jumlah[]")
                cursor.execute("SET search_path TO hidayf14")
                cursor.execute("INSERT INTO produksi VALUES (%s, %s, %s, %s)", [tool, food, duration, amount])
                for i in range(len(ingredient_list)):
                    cursor.execute("INSERT INTO PRODUK_DIBUTUHKAN_OLEH_PRODUK_MAKANAN VALUES (%s, %s, %s)", [food, ingredient_list[i], int(amount_list[i])])
                return redirect("product:list_production")
            else:
                cursor.execute("SET search_path TO hidayf14")
                cursor.execute("SELECT nama, id FROM PRODUK_MAKANAN INNER JOIN PRODUK ON produk_makanan.id_produk = produk.id")
                makanan = cursor.fetchall()
                cursor.execute("SELECT nama, id FROM alat_produksi INNER JOIN aset ON alat_produksi.id_aset = aset.id")
                alat = cursor.fetchall()
                cursor.execute("SELECT nama, id FROM PRODUK")
                bahan = cursor.fetchall()
                return render(request, 'form_produksi.html', {'makanan': makanan, 'alat': alat, 'bahan': bahan})
        else:
            return redirect("product:list_production")
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
        query = "SELECT pr.nama, a.nama, extract(epoch FROM x.durasi::interval)::int / 60 AS durasi, x.jumlah_unit_hasil, CASE "
        query += "WHEN exists(SELECT * FROM histori_produksi_makanan WHERE histori_produksi_makanan.id_alat_produksi = x.id_alat_produksi "
        query += "AND histori_produksi_makanan.id_produk_makanan = x.id_produk_makanan) THEN false ELSE true END "
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
        query = "SELECT pr.nama, a.nama, extract(epoch FROM x.durasi::interval)::int / 60 AS durasi, x.jumlah_unit_hasil, x.id_produk_makanan "
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

def update_production(request, id):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")

    if request.session.has_key('account'):
        role = request.session['role']
        if role == "admin":
            if request.method == "POST":
                food_id = request.POST["id_food"]
                tool_id = request.POST["id_tool"]
                duration = request.POST["duration"]
                duration = str(datetime.timedelta(seconds=(int(duration)*60)))
                amount = request.POST["amount"]
                cursor.execute("SET search_path TO hidayf14")
                cursor.execute("UPDATE PRODUKSI SET durasi = %s, jumlah_unit_hasil = %s WHERE id_alat_produksi LIKE %s AND id_produk_makanan LIKE %s", [duration, amount, tool_id, food_id])
                return redirect("product:list_production")
            else:
                cursor.execute("SET search_path TO hidayf14")
                query = "SELECT pr.nama, a.nama, x.durasi, x.jumlah_unit_hasil, x.id_produk_makanan, x.id_alat_produksi, x.id_produk_makanan "
                query += "FROM (SELECT * FROM produksi p, alat_produksi ap, produk_makanan pm "
                query += "WHERE p.id_alat_produksi = ap.id_aset and p.id_produk_makanan = pm.id_produk) "
                query += "x LEFT OUTER JOIN aset a ON x.id_alat_produksi = a.id LEFT OUTER JOIN produk pr ON x.id_produk_makanan = pr.id"
                cursor.execute(query)
                data = cursor.fetchall()
                selected_data = data[id-1]
                new_query = "SELECT p.nama, pd.jumlah "
                new_query += "FROM produk_dibutuhkan_oleh_produk_makanan pd LEFT OUTER JOIN produk p "
                new_query += "ON pd.id_produk = p.id "
                string = "WHERE pd.id_produk_makanan LIKE '%s'" % selected_data[4]
                new_query += string
                cursor.execute(new_query)
                detail_data = cursor.fetchall()
                return render(request, 'update_produksi.html', {'produksi': selected_data, 'bahan': detail_data})
        else:
            cursor.execute("SET search_path TO hidayf14")
            return redirect("product:list_production")
    else:
        return redirect("home:login")

def delete_production(request, id):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")

    if request.session.has_key('account'):
        role = request.session['role']
        if role == "admin":
            cursor.execute("SET search_path TO hidayf14")
            query = "SELECT pr.nama, a.nama, x.durasi, x.jumlah_unit_hasil, x.id_produk_makanan, x.id_alat_produksi, x.id_produk_makanan "
            query += "FROM (SELECT * FROM produksi p, alat_produksi ap, produk_makanan pm "
            query += "WHERE p.id_alat_produksi = ap.id_aset and p.id_produk_makanan = pm.id_produk) "
            query += "x LEFT OUTER JOIN aset a ON x.id_alat_produksi = a.id LEFT OUTER JOIN produk pr ON x.id_produk_makanan = pr.id"                
            cursor.execute(query)
            data = cursor.fetchall()
            selected_data = data[id-1]
            cursor.execute("DELETE FROM PRODUKSI WHERE id_alat_produksi LIKE %s AND id_produk_makanan LIKE %s", [selected_data[5], selected_data[6]])
            cursor.execute("DELETE FROM PRODUK_DIBUTUHKAN_OLEH_PRODUK_MAKANAN WHERE id_produk_makanan LIKE %s", [selected_data[6]])
            return redirect("product:list_production")

def create_product_history(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")

    if request.session.has_key('account'):
        role = request.session['role']
        if role == "pengguna":
            if request.method == "POST":
                food_id = request.POST["product"]
                amount = request.POST["amount"]
                cursor.execute("SET search_path TO hidayf14")
                cursor.execute("SELECT id_produk, jumlah FROM lumbung_memiliki_produk WHERE id_lumbung = %s", [request.session['account'][0]])
                available = cursor.fetchall()
                availability = {}
                for i in available:
                    availability[i[0]] = i[1]
                cursor.execute("SELECT id_produk, jumlah FROM produk_dibutuhkan_oleh_produk_makanan WHERE id_produk_makanan = %s", [food_id])
                ingredients = cursor.fetchall()
                for i in ingredients:
                    check = availability.get(i[0], None)
                    if check != None:
                        if availability[i[0]] >= int(i[1] * amount):
                            continue
                    messages.add_message(request, messages.INFO, 'Anda tidak memiliki bahan yang cukup, silahkan menambahkan produk yang akan digunakan sebagai bahan terlebih dahulu')
                    return redirect("product:create_product_history")
                cursor.execute("SELECT id_alat_produksi, durasi FROM produksi WHERE id_produk_makanan = %s", [food_id])
                tool = cursor.fetchone()
                cursor.execute("SELECT * FROM koleksi_aset_memiliki_aset WHERE id_koleksi_aset = %s AND id_aset = %s", [request.session['account'][0], tool[0]])
                exist = cursor.fetchone()
                if exist == None:
                    messages.add_message(request, messages.INFO, 'Anda tidak memiliki alat yang dibutuhkan')
                    return redirect("product:create_product_history")
                time = datetime.datetime.now()
                duration = datetime.timedelta(hours=tool[1].hour, minutes=tool[1].minute, seconds=tool[1].second)
                finished_time = time + duration
                # finished_time = time + datetime.timedelta(seconds=int(tool[1].total_seconds()))
                cursor.execute("INSERT INTO histori_produksi(EMAIL, WAKTU_AWAL, WAKTU_SELESAI, JUMLAH, XP) VALUES (%s, %s, %s, %s, %s)", [request.session['account'][0], time, finished_time , int(amount), int(amount)*5])
                cursor.execute("INSERT INTO histori_produksi_makanan VALUES(%s, %s, %s, %s)", [request.session['account'][0], time, tool[0], food_id])
                return redirect("product:list_history")
            else:
                cursor.execute("SET search_path TO hidayf14")
                cursor.execute("SELECT nama, id FROM PRODUK_MAKANAN INNER JOIN PRODUK ON produk_makanan.id_produk = produk.id")
                makanan = cursor.fetchall()
                return render(request, 'form_histori_produk.html', {'makanan':makanan})
        else:
            return redirect("product:list_history")
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
        cursor.execute("SET search_path TO hidayf14")
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