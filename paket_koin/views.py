from hashlib import new
import re
from django.db import connection
from django.shortcuts import redirect, render

# Create your views here.
def create_paket(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    
    if request.session.has_key('account'):
        role = request.session['role']
        if role == "admin":
            if request.method == "POST":
                value = request.POST["value"]
                price = request.POST["price"]
                
                # cursor.execute("SET search_path TO hidayf14")
                # cursor.execute("INSERT INTO paket_koin VALUES (%s, %s)", [value, price])
                return redirect("paket_koin:list_paket")
            else:
                return render(request, "create_paket.html", {})
        else:
            return redirect("paket_koin:list_paket")
    else:
        return redirect("home:login")


def list_paket(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
                
    if request.session.has_key('account'):
        if request.session['role'] == "admin":
            role = "admin"
        else:
            role = None
    
    cursor.execute("SET search_path TO hidayf14")
    cursor.execute("SELECT * FROM paket_koin")
    data = cursor.fetchall()
    return render(request, 'list_paket.html', {'data': data, 'role': role})

def update_paket(request, value, harga):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    
    if request.session.has_key('account'):
        role = request.session['role']
        if role == "admin":
            if request.method == "POST":
                return redirect("paket_koin:list_paket")
            else:
                return render(request, 'update_paket.html', {'value': value, 'role': role, 'harga':harga})
        else:
            return redirect("paket_koin:list_paket")
    else:
        return redirect("home:login")
    
def list_transaksi(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
                
    if request.session.has_key('account'):
        if request.session['role'] == "admin":
            role = "admin"
        else:
            role = None
    
    cursor.execute("SET search_path TO hidayf14")
    if role == "admin":
        cursor.execute("SELECT * FROM transaksi_pembelian_koin")
        data = cursor.fetchall()
    else:
        cursor.execute("SELECT * FROM transaksi_pembelian_koin WHERE email = '" + request.session['account'][0] + "'")
        data = cursor.fetchall()
        
    return render(request, 'list_transaksi.html', {'data': data, 'role': role})

def beli_paket_koin(request, value, harga):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    
    if request.session.has_key('account'):
        if request.session['role'] == "admin":
            role = "admin"
        else:
            role = None
            
        if role == None:
            if request.method == "POST":
                jumlah = request.POST["jumlah"]
                cara = request.POST["cara"]
                
                # cursor.execute("SET search_path TO hidayf14")
                # cursor.execute("INSERT INTO paket_koin VALUES (%s, %s)", [value, price])
                return redirect("paket_koin:list_transaksi")
            else:
                return render(request, "beli_paket_koin.html", {'value': value, 'role': role, 'harga': harga})
        else:
            return redirect("paket_koin:list_transaksi")
    else:
        return redirect("home:login")



