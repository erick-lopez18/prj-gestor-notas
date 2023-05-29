from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Vistas de la aplicación. Usar en conjunto con carpeta 'templates'.

# ELR: Función para índice de bienvenida. Usa template 'index.html'.
@login_required
def index(request):
    return render(request, "app/index.html")

# ELR: Función para login de usuario. Usa template 'login.html'.
def login_usuario(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('notas_usuario')
        else:
            messages.error(request, 'Credenciales inválidas.')
    return render(request, 'login.html')

# ELR: Función para menú CRUD. Usa template 'notas_usuario.html'.
@login_required
def notas_usuario(request):
    return render(request, 'notas_usuario.html')