from django import forms
from .models import Operacion

class Formulario(forms.ModelForm):
    class Meta:
        model = Operacion
        fields = '__all__'
