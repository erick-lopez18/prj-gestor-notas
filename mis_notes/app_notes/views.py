import logging
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.views.generic import TemplateView
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
from app_notes.forms import UserLoginForm, UserRegisterForm
from app_notes.models import Usuario, Nota, Evento

# Vistas de la aplicación. Usar en conjunto con carpeta 'templates'.

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

User = get_user_model()

# Serializer para los tokens de autentificación.
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer 

# ELR: Vista para índice de bienvenida.
#      La primera pantalla que el usuario ve al entrar a la aplicación.
def index(request):
    return render(request, "index.html")  # Usa template 'index.html'.

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

# ELR: Función para login de usuario.
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([AllowAny])
class LoginUsuarioViewSet(viewsets.ViewSet):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'login.html'

    def create(self, request):
        return self.handle_post(request)
    
    def handle_post(self, request):
        form = UserLoginForm(request.data)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(username=username)
                #user = User.objects.filter(Q(username=username).first() | Q(email=email))
                #user = User.objects.filter(Q(username=username) | Q(email=username)).first()
                if user.check_password(password):
                    login(request, user)
                    print(f"Inicio de sesión exitoso para el usuario: {username}")
                    ##refresh = RefreshToken.for_user(user)
                    #response_data = {
                    #    'refresh': str(refresh),
                    #    'access': str(refresh.access_token),
                    #    'redirect': 'home',
                    #}
                    messages.success(request, 'Inicio de sesión exitoso.')
                    
                    #return JsonResponse(response_data)
                    ##return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

                    # Utiliza el valor de 'next' si está presente, de lo contrario usa la configuración 'LOGIN_REDIRECT_URL'
                    #redirect_url = request.GET.get('next', settings.LOGIN_REDIRECT_URL)

                    # Redirige al usuario a la URL correspondiente después del inicio de sesión exitoso
                    #return redirect(redirect_url)
                    next_url = request.GET.get('next')
                    print(next_url)
                    if next_url is not None:
                        print(f'Se uso next_url')
                        return redirect(reverse(next_url))
                    else:
                        print(f'Se uso settings')
                        return HttpResponseRedirect(reverse(settings.LOGIN_REDIRECT_URL))
                else:
                    #return JsonResponse({'error': 'Credenciales inválidas.'}, status=401)
                    print('ay lmao credentials')
                    messages.error(request, 'Credenciales inválidas. Intenta de nuevo.')
                    logger.warning(f"Credenciales inválidas para el usuario: {username}")
                    #return redirect(self.url_name) 
                    return HttpResponseRedirect(settings.LOGIN_URL)
                    #return redirect('login')  # Redireccionar al template de login 401
            except User.DoesNotExist:
                #return JsonResponse({'error': 'El usuario no existe o las credenciales son inválidas.'}, status=400)
                print('ay lmao user')
                messages.error(request, 'El usuario no existe. Verifica tus credenciales.')
                logger.warning(f"El usuario no existe: {username}")
                #return redirect(self.url_name) 
                return HttpResponseRedirect(settings.LOGIN_URL)
                #return redirect('login')  # Redireccionar al template de login 400
        else:
            print('ay lmao form')
            messages.error(request, 'Formulario inválido.')
            logger.warning("Formulario de inicio de sesión inválido")
            #return redirect(self.url_name)
            return HttpResponseRedirect(settings.LOGIN_URL)
            #errors = form.errors.as_json()
            #return JsonResponse({'errors': errors}, status=400)
            #return Response({'form': form}, status=status.HTTP_400_BAD_REQUEST)
        
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
        form = UserLoginForm()
        #return redirect('login')
        return render(request, self.template_name, {'form': form})

# ELR: Función para registro de usuario.
#def registro_usuario(request):
#    if request.method == 'POST':
#        form = UserRegisterForm(request.POST)
#        if form.is_valid():
#            user = form.save()
#            # Acciones adicionales aqui
#            return redirect('login')  # Redirigir a vista de login.
#    else:
#        form = UserRegisterForm()
#    return render(request, 'register.html', {'form': form})  # Usa template ''.

@permission_classes([AllowAny])
class LoginUsuarioView(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        else:
            return redirect('login-view')

@permission_classes([AllowAny])
class RegistroUsuarioViewSet(viewsets.ViewSet):
    #def create(self, request, format=None):
    #    form = UserRegisterForm(request.data)
    #    if form.is_valid():
    #        user = form.save()
    #        refresh = RefreshToken.for_user(user)
    #        access_token = refresh.access_token
    #        return Response({
    #            'access_token': str(access_token),
    #            'refresh_token': str(refresh),
    #            'detail': 'Usuario registrado exitosamente.'
    #        })
    #    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'register.html'
    #url_name = 'register'

    def list(self, request):
        #form = UserRegisterForm()
        #self.handle_get(request)
        #return Response({'form': form})
        return self.handle_get(request)

    def create(self, request):
        #if request.method == 'POST':
        #    return self.handle_post(request)
        #elif request.method == 'GET':
        #    return Response({'detail': 'Método no permitido.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if request.method == 'POST':
            return self.handle_post(request)
        elif request.method == 'GET':
            return self.handle_get(request)
        else:
            return Response({'detail': 'Método no permitido.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def handle_post(self, request):
        form = UserRegisterForm(request.data)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Crea un objeto 'Usuario' con la ID del usuario registrado
            usuario = Usuario(username=user)
            usuario.save()
            messages.success(request, 'Usuario registrado exitosamente.')
            login_url = reverse('login-list')
            return redirect(login_url)
        return Response({'form': form}, status=status.HTTP_400_BAD_REQUEST)

    def handle_get(self, request):
        form = UserRegisterForm()
        return render(request, self.template_name, {'form': form})
        #return Response({'form': form})


# ELR: Prueba de activación manual de cuenta usuario
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

# ELR: Home
#@permission_classes([IsAuthenticated])
#def menu_home(request):
#    return render(request, 'home.html')

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.user.username
        context['next'] = self.request.GET.get('next', 'home')
        return context

class HomeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        context = {'username': request.user.username, 'message': 'Welcome to the API Home'}
        #return Response({'username': request.user.username, 'message': 'Welcome to the API Home'})
        return render(request, 'home.html', context)

    def post(self, request):
        return Response({'message': 'POST request processed'})

# ELR: Función para CRUD de notas.
#@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def menu_notas(request):
    if request.method == 'GET':
        notes = Nota.objects.filter(created_by=request.user)
        serializer = NoteSerializer(notes, many=True)
        return render(request, 'notes_menu.html', {'notes': serializer.data})  # Usa template 'notes.html'.
    return HttpResponse(status=405)  # Método no permitido (405) si no es una solicitud POST

# ELR: Detalle de notas
def detalle_nota(request, nota_id):
    note = get_object_or_404(Nota, id=nota_id)
    serializer = NoteSerializer(note, many=True)
    return render(request, 'notes_edit.html', {'note': serializer.data})

class NotasUsuarioViewSet(LoginRequiredMixin, viewsets.ViewSet):
    #permission_classes = [IsAuthenticated]
    #permission_classes = [AllowAny]

    def list(self, request):
        # Obtener el usuario actualmente autenticado
        usuario = request.user
        try:
            # Obtener la instancia de Usuario correspondiente al usuario actual
            usuario_instance = Usuario.objects.get(username=usuario)
            # Obtener las notas asociadas al usuario
            notas = Nota.objects.filter(usuario=usuario_instance)
            serializer = NoteSerializer(notas, many=True)
            if notas.exists():
                # Hay notas disponibles
                context = {'notas': serializer.data}
            else:
                # No hay notas disponibles
                context = {'mensaje': 'No hay notas disponibles'}
        except Usuario.DoesNotExist:
            # El usuario no tiene una instancia de Usuario asociada
            context = {'mensaje': 'No se encontró el usuario'}
        return render(request, 'notes_menu.html', context)

    def destroy(self, request, pk=None):
        # Obtén el ID de la nota a eliminar desde la solicitud POST
        nota_id = request.POST.get('nota_id')

        if nota_id:
            # Obtén la instancia de la nota a eliminar
            nota = get_object_or_404(Nota, id=nota_id, usuario__username=request.user.id)
        
            # Realiza la eliminación de la nota
            nota.delete()

        # Redirige a la página de notas nuevamente
        return HttpResponseRedirect(reverse('notes-menu-list'))


class DetalleNotaViewSet(LoginRequiredMixin, viewsets.ViewSet):
    #permission_classes = [IsAuthenticated]
    def list(self, request, pk=None):
        pass

    def create(self, request, pk=None):
        topic = request.data.get('topic')
        text = request.data.get('text')
        #usuario = request.user.username
        usuario = Usuario.objects.get(username=request.user.id)
        print(usuario)
        nota = Nota.objects.create(usuario=usuario, topico=topic, texto=text)
        serializer = NoteSerializer(nota)
        url = reverse('notes-detail', kwargs={'pk': nota.pk})
        return redirect(url)
        #return redirect('notes-detail', pk=nota.id)
        #note = Nota()
        #serializer = NoteSerializer(note)
        #topic = request.data.get('topic')
        #text = request.data.get('text')
        #usuario = Usuario.objects.get(usuario=request.user)
        #nota = Nota.objects.create(usuario=usuario, topico=topic, texto=text)
        #return render(request, 'notes_detail.html', {'note': serializer.data})

    def retrieve(self, request, pk=None):
        if pk is None:
            #note = Nota()
            note = None
        else:
            note = get_object_or_404(Nota, id=pk, usuario__username=request.user.id)
        serializer = NoteSerializer(note) if note else None
        return render(request, 'notes_detail.html', {'note': serializer.data if serializer else None})

    def update(self, request, pk=None):
        # Implementa la lógica para actualizar una nota existente
        pass

    def partial_update(self, request, pk=None):
        # Implementa la lógica para actualizar parcialmente una nota existente
        pass

# ELR: Función para CRUD de rventos.
#@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def menu_eventos(request):
    if request.method == 'GET':
        events = Evento.objects.filter(created_by=request.user)
        serializer = EventSerializer(events, many=True)
        return render(request, 'events_menu.html', {'events': serializer.data})
    return HttpResponse(status=405)  # Método no permitido (405) si no es una solicitud POST

class EventosUsuarioViewSet(viewsets.ViewSet):
    #permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def list(self, request):
        #events = Evento.objects.filter(created_by=request.user)
        username = request.user
        # Obtener la instancia de Usuario correspondiente al usuario actual
        usuario_instance = Usuario.objects.get(username=username)
        # Obtener los eventos asociadas al usuario
        eventos = Evento.objects.filter(usuario=usuario_instance)
        serializer = EventSerializer(eventos, many=True)

        if eventos.exists():
            serializer = EventSerializer(eventos, many=True)
            context = {'events': serializer.data}
        else:
            context = {'mensaje': 'No hay eventos disponibles'}

        return render(request, 'events_menu.html', context)

    def create(self, request):
        # Implementa la lógica para crear un nuevo evento
        pass

    def destroy(self, request, pk=None):
        # Implementa la lógica para eliminar un evento existente
        pass

class DetalleEventoViewSet(viewsets.ViewSet):
    #permission_classes = [IsAuthenticated]
    def create(self, request):
        # Implementa la lógica para crear un nuevo evento
        pass

    def retrieve(self, request, pk=None):
        event = get_object_or_404(Evento, id=pk, created_by=request.user)
        serializer = EventSerializer(event)
        return render(request, 'events_detail.html', {'event': serializer.data})

    def update(self, request, pk=None):
        # Implementa la lógica para actualizar una nota existente
        pass

    def partial_update(self, request, pk=None):
        # Implementa la lógica para actualizar parcialmente una nota existente
        pass