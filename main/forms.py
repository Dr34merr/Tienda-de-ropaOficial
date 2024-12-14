from django import forms
from .models import Producto
from .models import Cliente
from .models import User
from django.contrib.auth.forms import UserCreationForm

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'existecias', 'imagen']

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nombre", "email", "telefono"]  # Ajusta los campos según tu modelo

class UsuarioForm(UserCreationForm):
    class Meta:
        model = User  # Cambiar de Cliente a User
        fields = ["username", "password1", "password2"]