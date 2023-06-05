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
from app_notes.views import MyTokenObtainPairView
from app_notes.views import index, menu_notas, menu_eventos, detalle_nota
from app_notes.views import HomeView, HomeAPIView
from app_notes.views import LoginUsuarioViewSet, RegistroUsuarioViewSet
from app_notes.views import NotasUsuarioViewSet, DetalleNotaViewSet
from app_notes.views import EventosUsuarioViewSet, DetalleEventoViewSet

# ELR: Definición del router de Django REST framework.
router = DefaultRouter()

# ELR: Direcciones URL de Django para las vistas en 'views.py'.
#      'views.py' se encuentra dentro de la carpeta 'app_notes'.
#      Las vistas son definidas en 'from app_notes.views import ...'.
#      Esto debe cumplirse antes de usarlas en 'urlpatterns = []' con 'path()'.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('index')),
    path('index/', index, name='index'),
    # path('register/', registro_usuario, name='register'),
    path('home/', HomeView.as_view(), name='home'),
    #path('login/', LoginUsuarioView.as_view(), name='login-view'),
    path('api/home/', HomeAPIView.as_view(), name='api_home'),
    #path('menu/notes/', menu_notas, name='notes_menu'),
    path('notes/detail/<int:pk>/', DetalleNotaViewSet.as_view({'get': 'retrieve', 'post': 'create'}), name='notes-detail'),
    ###path('notes/detail/', DetalleNotaViewSet.as_view({'get': 'retrieve', 'post': 'create'}), name='notes-detail'),
    path('notes/detail/new/', DetalleNotaViewSet.as_view({'get': 'retrieve', 'post': 'create'}), name='notes-new'),
    ##path('notes/detail/new/', DetalleNotaViewSet.as_view({'post': 'create'}), name='notes-create'),
    ##path('notes/detail/<int:pk>/', DetalleNotaViewSet.as_view({'get': 'retrieve'}), name='notes-detail'),
    #path('menu/notes/edit/<int:nota_id>/', detalle_nota, name='notes_edit'),
    #path('menu/events/', menu_eventos, name='events_menu'),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]

# ELR: Direcciones URL de vistas que utilizan el enrutador de Django REST framework.
#      Pasan por el mismo procedimiento que 'urlpatterns = []' indicado anteriormente.
#      Las vistas son construídas como clases antes de usarlas con 'router.register()'. 
router.register(r'login', LoginUsuarioViewSet, basename='login')
router.register(r'register', RegistroUsuarioViewSet, basename='register')
router.register(r'notes/menu', NotasUsuarioViewSet, basename='notes-menu')
#router.register(r'notes/detail', DetalleNotaViewSet, basename='notes-detail')
router.register(r'events/menu', EventosUsuarioViewSet, basename='events-menu')
router.register(r'events/detail', DetalleEventoViewSet, basename='events-detail')

# ELR: Esta línea integra todas las URLs creadas en el enrutador de DRF hacia 'urlpatterns'.
urlpatterns += router.urls