from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
# from django.http import HttpResponse

## Hola, esto es un sistema gestor notas. Esto se muestra al levantar entorno.
# def bienvenida(request):
#    return HttpResponse("Bienvenido al sistema gestor de notas.")
# Indice de bienvenida (index.html)
@login_required
def index(request):
    return render(request, "app/index.html")

# Login de usuario 
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

# Vista CRUD
@login_required
def notas_usuario(request):
    return render(request, 'notas_usuario.html')