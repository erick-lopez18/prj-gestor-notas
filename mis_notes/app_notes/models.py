from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        if not username:
            raise ValueError('El campo de nombre de usuario debe ser proporcionado')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True, default='default_username')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    objects = UserManager()

    def __str__(self):
        return self.username
    
class Usuario(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.username.username

class Nota(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='notas')
    topico = models.CharField(max_length=100)
    texto = models.TextField()

    def __str__(self):
        return self.topico

class Evento(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='eventos')
    topico = models.CharField(max_length=100)
    notas = models.TextField()

    def __str__(self):
        return self.topico
