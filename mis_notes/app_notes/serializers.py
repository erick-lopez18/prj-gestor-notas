from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

User = get_user_model()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': ('No se encontró una cuenta activa con las credenciales proporcionadas.'),
        'invalid_credentials': ('Credenciales inválidas.')
    }
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Puedes agregar información adicional al token aquí si lo deseas
        # Por ejemplo, puedes incluir el nombre de usuario en los datos del token
        token['username'] = user.username

        return token
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = User.objects.filter(Q(username=username) | Q(email=username)).first()

        if user and user.check_password(password):
            if not user.is_active:
                raise serializers.ValidationError(self.error_messages['no_active_account'])
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError(self.error_messages['invalid_credentials'])


class NoteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    topic = serializers.CharField(max_length=255)
    text = serializers.CharField()
    created_by = serializers.ReadOnlyField(source='created_by.username')

class EventSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    topic = serializers.CharField(max_length=255)
    notes = serializers.CharField()
    created_by = serializers.ReadOnlyField(source='created_by.username')