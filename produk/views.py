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
                return redirect("produk:list_product")
            
            else:
                return render(request, "form_produk.html", {})
            
        else:
            return redirect("produk:list_product")
    else:
        return redirect("home:login")

def read_product(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")

    if request.session.has_key('account'):
        if request.session['role'] == "admin":
            role = "admin"
        
        cursor.execute("SET search_path TO hidayf14")
        cursor.execute("SELECT * FROM produk")
        data = cursor.fetchall()
        print(data)
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
                return redirect("produk:list_product")
            else:
                return render(request, 'update_produk.html', {})
        else:
            return redirect("produk:list_product")
    else:
        return redirect("home:login")