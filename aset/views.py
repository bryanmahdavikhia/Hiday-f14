
from hashlib import new
from django.db import connection
from django.shortcuts import redirect, render


def index(request):
    return render(request, 'createAsset.html')

def pilihan_list_koleksi_aset(request):
    return render(request, 'list_pilihan_koleksi_aset.html')

def form_bibit_tanaman(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('account'):
        role = request.session['role']
        if role == "admin":
            if request.method == "POST":
                nama = request.POST.get("nama")
                min_level = request.POST.get("min_level")
                harga_beli = request.POST.get("harga_beli")
                durasi_panen = request.POST.get("durasi_panen")
                cursor.execute("SET search_path TO hidayf14")
                cursor.execute("SELECT id FROM aset WHERE id LIKE '%BT%' ORDER BY id DESC LIMIT 1")
                id = cursor.fetchone()
                if id is None:
                    id = "BT001"
                else:
                    id = str(id)
                    id = "BT" + str(int(id[4:7]) + 1).zfill(3)
                cursor.execute("INSERT INTO aset VALUES (%s, %s, %s, %s)", [id, nama, min_level, harga_beli])
                cursor.execute("INSERT INTO bibit_tanaman VALUES (%s, %s)", [id, durasi_panen])
                return redirect("aset:list-bibit-tanaman")
            else:
                return render(request, 'form_bibit_tanaman.html')

def form_dekorasi(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('account'):
        role = request.session['role']
        if role == "admin":
            if request.method == "POST":
                nama = request.POST.get("nama")
                min_level = request.POST.get("min_level")
                harga_beli = request.POST.get("harga_beli")
                harga_jual = request.POST.get("harga_jual")
                cursor.execute("SET search_path TO hidayf14")
                cursor.execute("SELECT id FROM aset WHERE id LIKE '%DK%' ORDER BY id DESC LIMIT 1")
                id = cursor.fetchone()
                if id is None:
                    id = "DK001"
                else:
                    id = str(id)
                    id = "DK" + str(int(id[4:7]) + 1).zfill(3)
                cursor.execute("INSERT INTO aset VALUES (%s, %s, %s, %s)", [id, nama, min_level, harga_beli])
                cursor.execute("INSERT INTO dekorasi VALUES (%s, %s)", [id, harga_jual])
                return redirect("aset:list-dekorasi")
            else:
                return render(request, 'form_dekorasi.html')

def form_kandang(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('account'):
        role = request.session['role']
        if role == "admin":
            if request.method == "POST":
                nama = request.POST.get("nama")
                min_level = request.POST.get("min_level")
                harga_beli = request.POST.get("harga_beli")
                kapasitas_maks = request.POST.get("kapasitas_maks")
                jenis_hewan = request.POST.get("jenis_hewan")
                cursor.execute("SET search_path TO hidayf14")
                cursor.execute("SELECT id FROM aset WHERE id LIKE '%KD%' ORDER BY id DESC LIMIT 1")
                id = cursor.fetchone()
                if id is None:
                    id = "KD001"
                else:
                    id = str(id)
                    id = "KD" + str(int(id[4:7]) + 1).zfill(3)
                cursor.execute("INSERT INTO aset VALUES (%s, %s, %s, %s)", [id, nama, min_level, harga_beli])
                cursor.execute("INSERT INTO kandang VALUES (%s, %s, %s)", [id, kapasitas_maks, jenis_hewan])
                return redirect("aset:list-kandang")
            else:
                return render(request, 'form_kandang.html')

def form_hewan(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('account'):
        role = request.session['role']
        if role == "admin":
            if request.method == "POST":
                nama = request.POST.get("nama")
                min_level = request.POST.get("min_level")
                harga_beli = request.POST.get("harga_beli")
                durasi_produksi = request.POST.get("durasi_produksi")
                cursor.execute("SET search_path TO hidayf14")
                cursor.execute("SELECT id FROM aset WHERE id LIKE '%HW%' ORDER BY id DESC LIMIT 1")
                id = cursor.fetchone()
                if id is None:
                    id = "HW001"
                else:
                    id = str(id)
                    id = "HW" + str(int(id[4:7]) + 1).zfill(3)
                cursor.execute("INSERT INTO aset VALUES (%s, %s, %s, %s)", [id, nama, min_level, harga_beli])
                cursor.execute("INSERT INTO hewan VALUES (%s, %s)", [id, durasi_produksi])
                return redirect("aset:list-hewan")
            else:
                return render(request, 'form_hewan.html')

def form_alat_produksi(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('account'):
        role = request.session['role']
        if role == "admin":
            if request.method == "POST":
                nama = request.POST.get("nama")
                min_level = request.POST.get("min_level")
                harga_beli = request.POST.get("harga_beli")
                kapasitas_maks = request.POST.get("kapasitas_maks")
                cursor.execute("SET search_path TO hidayf14")
                cursor.execute("SELECT id FROM aset WHERE id LIKE '%AP%' ORDER BY id DESC LIMIT 1")
                id = cursor.fetchone()
                if id is None:
                    id = "AP001"
                else:
                    id = str(id)
                    id = "AP" + str(int(id[4:7]) + 1).zfill(3)
                cursor.execute("INSERT INTO aset VALUES (%s, %s, %s, %s)", [id, nama, min_level, harga_beli])
                cursor.execute("INSERT INTO alat_produksi VALUES (%s, %s)", [id, kapasitas_maks])
                return redirect("aset:list-alat")
            else:
                return render(request, 'form_alat_produksi.html')

def form_petak_sawah(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('account'):
        role = request.session['role']
        if role == "admin":
            if request.method == "POST":
                nama = request.POST.get("nama")
                min_level = request.POST.get("min_level")
                harga_beli = request.POST.get("harga_beli")
                jenis_tanaman = request.POST.get("jenis_tanaman")
                cursor.execute("SET search_path TO hidayf14")
                cursor.execute("SELECT id FROM aset WHERE id LIKE '%PS%' ORDER BY id DESC LIMIT 1")
                id = cursor.fetchone()
                if id is None:
                    id = "PS001"
                else:
                    id = str(id)
                    id = "PS" + str(int(id[4:7]) + 1).zfill(3)
                cursor.execute("INSERT INTO aset VALUES (%s, %s, %s, %s)", [id, nama, min_level, harga_beli])
                cursor.execute("INSERT INTO petak_sawah VALUES (%s, %s)", [id, jenis_tanaman])
                return redirect("aset:list-petak-sawah")
            else:
                cursor.execute("SET search_path TO hidayf14")
                cursor.execute("SELECT nama FROM aset, bibit_tanaman WHERE id=id_aset;")
                data = cursor.fetchall()
                return render(request, 'form_petak_sawah.html',{"data":data})

def form_beli_aset(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('account'):
        role = request.session['role']
        if role == "pengguna":
            if request.method == "POST":
                detail_aset = request.POST["detail_aset"]
                jumlah = request.POST["jumlah"]
            else:
                cursor.execute("SET search_path TO hidayf14") #harus dicek lagi
                list_aset = "SELECT nama, harga_beli FROM aset;"
                cursor.execute(list_aset)
                data = cursor.fetchall()
                return render(request, 'form_beli_aset.html',{"dropDownAset":data})

def list_transaksi_pembelian_aset(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public") 
    if request.session.has_key('account'):
        if request.session['role'] == "admin":
            role = "admin"
        else:
            role = None
    cursor.execute("SET search_path TO hidayf14") 

    list_aset = "SELECT email, waktu, nama, jumlah, jumlah*harga_beli AS total_harga FROM aset,transaksi_pembelian WHERE id=id_aset;"
    cursor.execute(list_aset)
    data = cursor.fetchall()
    return render(request, 'list_transaksi_beli_aset.html',{"data":data,'role': role})

def list_aset(request):
    return render(request, 'list_aset.html')

def list_koleksi_dekorasi(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")

    if request.session.has_key('account'):
        if request.session['role'] == "admin":
            role = "admin"
        else:
            role = None
    cursor.execute("SET search_path TO hidayf14") 

    list_aset = "SELECT email, nama, minimum_level, harga_beli, jumlah FROM aset, koleksi_aset_memiliki_aset, pengguna WHERE email=id_koleksi_aset AND id=id_aset AND id_aset LIKE '%DK%';"
    cursor.execute(list_aset)
    data = cursor.fetchall()
    return render(request, 'list_koleksi_dekorasi.html', {'data': data, 'role': role})
        

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

def list_koleksi_bibit(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")

    if request.session.has_key('account'):
        if request.session['role'] == "admin":
            role = "admin"
        else:
            role = None
    cursor.execute("SET search_path TO hidayf14") 

    list_aset = "SELECT email, nama, minimum_level, harga_beli, jumlah FROM aset, koleksi_aset_memiliki_aset, pengguna WHERE email=id_koleksi_aset AND id=id_aset AND id_aset LIKE '%BT%';"
    cursor.execute(list_aset)
    data = cursor.fetchall()
    return render(request, 'list_koleksi_bibit.html', {'data': data, 'role': role})

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

def list_koleksi_kandang(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")

    if request.session.has_key('account'):
        if request.session['role'] == "admin":
            role = "admin"
        else:
            role = None
    cursor.execute("SET search_path TO hidayf14") 

    list_aset = "SELECT email, nama, minimum_level, harga_beli, jumlah FROM aset, koleksi_aset_memiliki_aset, pengguna WHERE email=id_koleksi_aset AND id=id_aset AND id_aset LIKE '%KD%';"
    cursor.execute(list_aset)
    data = cursor.fetchall()
    return render(request, 'list_koleksi_kandang.html', {'data': data, 'role': role})

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

def list_koleksi_hewan(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")

    if request.session.has_key('account'):
        if request.session['role'] == "admin":
            role = "admin"
        else:
            role = None
    cursor.execute("SET search_path TO hidayf14") 

    list_aset = "SELECT email, nama, minimum_level, harga_beli, jumlah FROM aset, koleksi_aset_memiliki_aset, pengguna WHERE email=id_koleksi_aset AND id=id_aset AND id_aset LIKE '%HW%';"
    cursor.execute(list_aset)
    data = cursor.fetchall()
    return render(request, 'list_koleksi_kandang.html', {'data': data, 'role': role})

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

def list_koleksi_alat_produksi(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")

    if request.session.has_key('account'):
        if request.session['role'] == "admin":
            role = "admin"
        else:
            role = None
    cursor.execute("SET search_path TO hidayf14") 

    list_aset = "SELECT email, nama, minimum_level, harga_beli, jumlah FROM aset, koleksi_aset_memiliki_aset, pengguna WHERE email=id_koleksi_aset AND id=id_aset AND id_aset LIKE '%AP%';"
    cursor.execute(list_aset)
    data = cursor.fetchall()
    return render(request, 'list_koleksi_alat.html', {'data': data, 'role': role})

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

def list_koleksi_petak_sawah(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")

    if request.session.has_key('account'):
        if request.session['role'] == "admin":
            role = "admin"
        else:
            role = None
    cursor.execute("SET search_path TO hidayf14") 

    list_aset = "SELECT email, nama, minimum_level, harga_beli, jumlah FROM aset, koleksi_aset_memiliki_aset, pengguna WHERE email=id_koleksi_aset AND id=id_aset AND id_aset LIKE '%PS%';"
    cursor.execute(list_aset)
    data = cursor.fetchall()
    return render(request, 'list_koleksi_alat.html', {'data': data, 'role': role})


def update_dekorasi(request, nama, id, min_level, harga_beli, harga_jual):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('account'):
        if request.session['role'] == "admin":
            if request.method == "POST":
                id_dekorasi = request.POST.get("id")
                nama = request.POST.get("nama")
                min_level = request.POST.get("min_level")
                harga_beli = request.POST.get("harga_beli")
                harga_jual = request.POST.get("harga_jual")
                cursor.execute("SET search_path TO hidayf14")
                cursor.execute("UPDATE aset SET minimum_level = %s, harga_beli = %s WHERE id = %s", [int(min_level), int(harga_beli), id_dekorasi])
                cursor.execute("UPDATE dekorasi SET harga_jual = %s WHERE id_aset = %s", [int(harga_jual), id_dekorasi])
                return redirect("aset:list-dekorasi")
            else:
                return render(request, 'update_dekorasi.html', {'id': id, 'nama': nama, 'min_level': min_level, 'harga_beli': harga_beli, 'harga_jual': harga_jual, 'role': request.session['role']})
        else:
            return redirect("aset:list-dekorasi")

def update_bibit(request, nama, id, min_level, harga_beli):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('account'):
        if request.session['role'] == "admin":
            if request.method == "POST":
                id_bibit_tanaman = request.POST.get("id")
                nama = request.POST.get("nama")
                min_level = request.POST.get("min_level")
                harga_beli = request.POST.get("harga_beli")
                cursor.execute("SET search_path TO hidayf14")
                cursor.execute("UPDATE aset SET minimum_level = %s, harga_beli = %s WHERE id = %s", [int(min_level), int(harga_beli), id_bibit_tanaman])
                return redirect("aset:list-bibit-tanaman")
            else:
                return render(request, 'update_bibit_tanaman.html', {'id': id, 'nama': nama, 'min_level': min_level, 'harga_beli': harga_beli, 'role': request.session['role']})
        else:
            return redirect("aset:list-bibit-tanaman")

def update_kandang(request, nama, id, min_level, harga_beli, kapasitas_maks, jenis_hewan):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('account'):
        if request.session['role'] == "admin":
            if request.method == "POST":
                id_kandang = request.POST.get("id")
                nama = request.POST.get("nama")
                min_level = request.POST.get("min_level")
                harga_beli = request.POST.get("harga_beli")
                kapasitas_maksimal = request.POST.get("kapasitas_maks")
                cursor.execute("SET search_path TO hidayf14")
                cursor.execute("UPDATE aset SET minimum_level = %s, harga_beli = %s WHERE id = %s", [int(min_level), int(harga_beli), id_kandang])
                cursor.execute("UPDATE kandang SET kapasitas_maks = %s WHERE id_aset = %s", [kapasitas_maksimal, id_kandang])
                return redirect("aset:list-kandang")
            else:
                return render(request, 'update_kadandang.html', {'id': id, 'nama': nama, 'min_level': min_level, 'harga_beli': harga_beli, 'kapasitas_maks': kapasitas_maks, 'jenis_hewan': jenis_hewan, 'role': request.session['role']})
        else:
            return redirect("aset:list-kandang")

def update_hewan(request, nama, id, min_level, harga_beli, id_kandang):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('account'):
        if request.session['role'] == "admin":
            if request.method == "POST":
                id_hewan = request.POST.get("id")
                nama = request.POST.get("nama")
                min_level = request.POST.get("min_level")
                harga_beli = request.POST.get("harga_beli")
                durasi_produksi = request.POST.get("durasi_produksi")
                id_kandang = request.POST.get("id_kandang")
                cursor.execute("SET search_path TO hidayf14")
                cursor.execute("UPDATE aset SET minimum_level = %s, harga_beli = %s WHERE id = %s", [int(min_level), int(harga_beli), id_hewan])
                return redirect("aset:list-hewan")
            else:
                return render(request, 'update_hewan.html', {'id': id, 'nama': nama, 'min_level': min_level, 'harga_beli': harga_beli, 'id_kandang': id_kandang, 'role': request.session['role']})
        else:
            return redirect("aset:list-hewan")

def update_alat(request, nama, id, min_level, harga_beli, kapasitas_maks):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('account'):
        if request.session['role'] == "admin":
            if request.method == "POST":
                id_alat = request.POST.get("id")
                nama = request.POST.get("nama")
                min_level = request.POST.get("min_level")
                harga_beli = request.POST.get("harga_beli")
                kapasitas_maksimal = request.POST.get("kapasitas_maks")
                cursor.execute("SET search_path TO hidayf14")
                cursor.execute("UPDATE aset SET minimum_level = %s, harga_beli = %s WHERE id = %s", [int(min_level), int(harga_beli), id_alat])
                cursor.execute("UPDATE alat_produksi SET kapasitas_maks = %s WHERE id_aset = %s", [kapasitas_maksimal, id_alat])
                return redirect("aset:list-alat")
            else:
                return render(request, 'update_alat_produksi.html', {'id': id, 'nama': nama, 'min_level': min_level, 'harga_beli': harga_beli, 'kapasitas_maks': kapasitas_maks, 'role': request.session['role']})
        else:
            return redirect("aset:list-alat")

def update_petak_sawah(request, nama, id, min_level, harga_beli):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('account'):
        if request.session['role'] == "admin":
            if request.method == "POST":
                id_petak_sawah = request.POST.get("id")
                nama = request.POST.get("nama")
                min_level = request.POST.get("min_level")
                harga_beli = request.POST.get("harga_beli")
                cursor.execute("SET search_path TO hidayf14")
                cursor.execute("UPDATE aset SET minimum_level = %s, harga_beli = %s WHERE id = %s", [int(min_level), int(harga_beli), id_petak_sawah])
                return redirect("aset:list-petak-sawah")
            else:
                return render(request, 'update_petak_sawah.html', {'id': id, 'nama': nama, 'min_level': min_level, 'harga_beli': harga_beli, 'role': request.session['role']})
        else:
            return redirect("aset:list-petak-sawah")
    
