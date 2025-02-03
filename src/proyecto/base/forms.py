from django import forms
from django.contrib.auth.models import User
from .models import Tarea, Categoria, Etiqueta

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'completo', 'categoria', 'etiquetas']
        widgets = {
            'etiquetas': forms.CheckboxSelectMultiple(),  # Permite seleccionar múltiples etiquetas
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']

class EtiquetaForm(forms.ModelForm):
    class Meta:
        model = Etiqueta
        fields = ['nombre']

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_superuser']