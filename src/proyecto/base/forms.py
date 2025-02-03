from django import forms
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