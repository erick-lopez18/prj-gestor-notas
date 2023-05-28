from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

## Hola, esto es un sistema gestor notas. Esto se muestra al levantar entorno.
def bienvenida(request):
    return HttpResponse("Bienvenido al sistema gestor de notas.")
