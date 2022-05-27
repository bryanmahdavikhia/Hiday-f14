from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import messages


def home(request):
    if not request.session.has_key('account'):
        return render(request, 'home.html')
    return redirect("home:main")

def login(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")

    if not request.session.has_key('account'):
        cursor.execute("SET search_path TO hidayf14")
        if request.method == "POST":
            email = request.POST["email"]
            password = request.POST["password"]
            cursor.execute("SELECT email FROM akun WHERE email = %s", [email])
            target = cursor.fetchone()

            if target is not None:
                cursor.execute("SELECT email FROM admin WHERE email = %s", [email])
                admin_check = cursor.fetchone()

                cursor.execute("SELECT email FROM pengguna WHERE email = %s", [email])
                pengguna_check = cursor.fetchone()

                if admin_check is not None:
                    role = "admin"
                    account = admin_check
                    cursor.execute("SELECT email, password FROM admin WHERE email = %s AND password = %s", [email, password])
                else:
                    role = "pengguna"
                    account = pengguna_check
                    cursor.execute("SELECT email, password FROM pengguna WHERE email = %s AND password = %s", [email, password])
                
                if cursor.fetchone() is not None:
                    cursor.execute("SET search_path TO public")
                    request.session['account'] = account
                    request.session['role'] = role
                    return HttpResponseRedirect("/main")
            
            messages.add_message(request, messages.INFO, 'Email atau password anda salah')
            cursor.execute("SET search_path TO public")
            return redirect("home:login")
        else:
            cursor.execute("SET search_path TO public")
            return render(request, "login.html", {})
    else:
        return redirect("home:main")

def main(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if request.session.has_key('account'):
        email = request.session['account'][0]
        if request.session['role'] == "admin":
            farm_details = None
        else:
            cursor.execute("SET search_path TO hidayf14")
            cursor.execute("SELECT * FROM PENGGUNA WHERE email = %s", [email])
            farm_details = cursor.fetchall()
        return render(request, 'main.html', {'email':email, 'farm_details':farm_details})
    else:
        return redirect("home:login")

def logout(request):
    try:
        del request.session['account']
        del request.session['role']
    except:
        pass
    return HttpResponseRedirect("/")

def register_option(request):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")
    if not request.session.has_key('account'):
        return render(request, 'role.html', {})
    else: 
        return redirect("home:main")

def register(request, id):
    cursor = connection.cursor()
    cursor.execute("SET search_path TO public")

    if not request.session.has_key('account'):
        cursor.execute("SET search_path TO hidayf14")
        if request.method == "POST":
            email = request.POST["email"]
            password = request.POST["password"]
            farm_name = request.POST["farm_name"]
            cursor.execute("SELECT email FROM akun WHERE email = %s", [email])
            target = cursor.fetchone()
            if target == None:
                cursor.execute("INSERT INTO akun VALUES (%s)", [email])
                if id == "admin":
                    cursor.execute("INSERT INTO admin VALUES (%s, %s)", [email, password])
                else:
                    cursor.execute("INSERT INTO pengguna VALUES (%s, %s, %s)", [email, password, farm_name])
                cursor.execute("SET search_path TO public")
                request.session['account'] = [email]
                request.session['role'] = id
                return HttpResponseRedirect("/main")
            else:
                messages.add_message(request, messages.INFO, 'Email sudah terambil. silahkan gunakan email lain')
                return redirect("home:register")
        else:
            if id == "admin":
                user = None
            else:
                user = "exist"
            return render(request, 'register.html', {'user':user})
    else:
        return redirect("home:main")
