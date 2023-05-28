"""
URL configuration for mis_notes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from app_notes.views import index, login_usuario, notas_usuario

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('index')),
    path('index/', index, name='index'),
    path('login/', login_usuario, name='login'),
    path('notas_usuario/', notas_usuario, name='notas_usuario')
]
