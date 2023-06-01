from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework.views import APIView
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import status, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from app_notes.serializers import MyTokenObtainPairSerializer, NoteSerializer, EventSerializer
from app_notes.forms import UserRegistrationForm
from app_notes.models import Nota, Evento

# Vistas de la aplicación. Usar en conjunto con carpeta 'templates'.

# Serializer para los tokens de autentificación.
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer 

# ELR: Función para índice de bienvenida.
def index(request):
    return render(request, "index.html")  # Usa template 'index.html'.

# ELR: Función para login de usuario.
#def login_usuario(request):
#    if request.method == 'POST':
#        username = request.POST['username']
#        password = request.POST['password']
#        user = authenticate(username=username, password=password)
#        if user is not None:
#            login(request, user)
#            return redirect('notas_usuario')  # Redirigir a vista de notas.
#        else:
#            messages.error(request, 'Credenciales inválidas.')
#    return render(request, 'login.html')  # Usar template 'login.html'.

#class LoginUsuarioAPIView(APIView):
#    #@action(detail=False, methods=['post'])
#    def post(self, request):
#        # username = request.POST.get('username')
#        # password = request.POST.get('password')
#        username = request.data.get['username']
#        password = request.data.get['password']
#        user = authenticate(username=username, password=password)
#        if user is not None:
#            return redirect('notas_usuario')  # Redirigir a vista de notas.
#        else:
#            return Response({'detail': 'Inicio de sesión exitoso.'})
#            # return Response({'error': 'Credenciales inválidas.'}, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([AllowAny])
class LoginUsuarioViewSet(viewsets.ViewSet):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'login.html'

    def create(self, request):
        return self.handle_post(request)
    
    def handle_post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = User.objects.get(username=username)
        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'detail': 'Credenciales inválidas.'}, status=401)
        
    ##def create(self, request):
        # username = request.data.get('username')
        # password = request.data.get('password')
        ##username = request.data['username']
        ##password = request.data['password']
        #user = authenticate(username=username, password=password)
        ##user = User.objects.get(username=username)
        #if user is not None:
        #    return redirect('notas_usuario')  # Redirigir a vista de notas.
        #else:
        #    return Response({'detail': 'Inicio de sesión exitoso.'},)
        ##if user.check_password(password):
            ##refresh = RefreshToken.for_user(user)
            ##return Response({
                ##'refresh': str(refresh),
                ##'access': str(refresh.access_token),
            ##})
        ##else:
            ##return Response({'detail': 'Credenciales inválidas.'}, status=401)
            # return Response({'error': 'Credenciales inválidas.'}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        return self.handle_get(request)
    
    def handle_get(self, request):
        #return redirect('login')
        return render(request, self.template_name)

# ELR: Función para registro de usuario.
User = get_user_model()
#def registro_usuario(request):
#    if request.method == 'POST':
#        form = UserRegistrationForm(request.POST)
#        if form.is_valid():
#            user = form.save()
#            # Acciones adicionales aqui
#            return redirect('login')  # Redirigir a vista de login.
#    else:
#        form = UserRegistrationForm()
#    return render(request, 'register.html', {'form': form})  # Usa template ''.

class RegistroUsuarioViewSet(viewsets.ViewSet):
    def create(self, request, format=None):
        form = UserRegistrationForm(request.data)
        if form.is_valid():
            user = form.save()
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            return Response({
                'access_token': str(access_token),
                'refresh_token': str(refresh),
                'detail': 'Usuario registrado exitosamente.'
            })
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


# Probando activacion de usuario
account_activation_token = PasswordResetTokenGenerator()
def activate_account(request, uidb64, token):
    try:
        uid = str(urlsafe_base64_decode(uidb64), 'utf-8')
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'registration/account_activated.html')
    else:
        return render(request, 'registration/activation_error.html')

# ELR: Función para CRUD de notas.
#@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notas_usuario(request):
    if request.method == 'GET':
        notes = Nota.objects.filter(created_by=request.user)
        serializer = NoteSerializer(notes, many=True)
        return render(request, 'notes.html', {'notas': serializer.data})  # Usa template 'notes.html'.
    return HttpResponse(status=405)  # Método no permitido (405) si no es una solicitud POST

# ELR: Función para CRUD de rventos.
#@api_view(['GET'])
@permission_classes([IsAuthenticated])
def events(request):
    if request.method == 'GET':
        events = Evento.objects.filter(created_by=request.user)
        serializer = EventSerializer(events, many=True)
        return render(request, 'events.html', {'eventos': serializer.data})
    return HttpResponse(status=405)  # Método no permitido (405) si no es una solicitud POST