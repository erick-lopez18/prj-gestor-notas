from django import forms
from app_notes.models import User

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        # Validar las credenciales aquí según tus requisitos
        user = User.objects.filter(username=username).first()
        if not user or not user.check_password(password):
            raise forms.ValidationError('Credenciales inválidas.')

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']