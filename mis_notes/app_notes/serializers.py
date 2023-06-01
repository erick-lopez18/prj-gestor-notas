from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Puedes agregar información adicional al token aquí si lo deseas
        # Por ejemplo, puedes incluir el nombre de usuario en los datos del token
        token['username'] = user.username

        return token

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