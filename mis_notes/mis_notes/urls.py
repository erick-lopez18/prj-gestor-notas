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
from django.urls import path, include
from django.shortcuts import redirect
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from app_notes.views import index, notas_usuario, events
from app_notes.views import MyTokenObtainPairView, LoginUsuarioViewSet, RegistroUsuarioViewSet

# Definición del router de Django REST framework
router = DefaultRouter()

# ELR: Direcciones URL para las funciones de vistas en 'views.py'.
#      'views.py' se encuentra dentro de la carpeta 'app_notes'.
#      Las funciones deben ser definidas en 'from app_notes.views import ...'.
#      Esto debe cumplirse antes de usarlas en 'urlpatterns = []' con 'path()'.
urlpatterns = [
    path('admin/', admin.site.urls),
    #
    path('', lambda request: redirect('index')),
    path('index/', index, name='index'),
    #
    # path('register/', registro_usuario, name='register'),
    path('notes/', notas_usuario, name='notes'),
    path('events/', events, name='events'),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    # path('login/', LoginUsuarioAPIView.as_view(), name='login'),
]

# ELR: Direcciones URL de funciones que pasan por el enrutador de Django REST framework.
#      Pasan por el mismo procedimiento que 'urlpatterns = []' indicado anteriormente.
#      Funciones aquí son escritas como clases antes de usarlas con 'router.register()'. 
router.register(r'login', LoginUsuarioViewSet, basename='login')
#router.register(r'login', LoginUsuarioAPIView, basename='login')
router.register('registro', RegistroUsuarioViewSet, basename='registro')
urlpatterns += router.urls