from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('main', views.main, name = 'main'),
    path('logout', views.logout, name = 'logout'),
    path('role', views.register_option, name = 'role'),
    path('register/<str:id>', views.register, name = 'register')
]
