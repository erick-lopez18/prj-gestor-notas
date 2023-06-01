from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', False)
        if not email:
            raise ValueError('El campo de correo electrónico debe ser proporcionado')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    objects = UserManager()

class Nota(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    topico = models.CharField(max_length=100)
    texto = models.TextField()

    def __str__(self):
        return self.topic

class Evento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    topico = models.CharField(max_length=100)
    notas = models.TextField()

    def __str__(self):
        return self.topic
