from django import forms
import datetime
from django.forms import TextInput
from .models import *


class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        exclude = ['fechaEgreso', 'usuario']
        widgets = {
            'nombre': forms.TextInput(),
            'apellido': forms.TextInput(),
            'fechaIngreso': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fechaNacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super(EmpleadoForm, self).__init__(*args, **kwargs)
        self.fields['cargo'].queryset = Cargo.objects.order_by('nivel__valor')
        # Transformar el texto de las opciones del campo cargo
        self.fields['cargo'].choices = [
            (option_value, option_label.title())  # Aplicar title() a cada opción
            for option_value, option_label in self.fields['cargo'].choices
        ]

class PeriodoForm(forms.ModelForm):
    class Meta:
        model = Periodo
        fields = '__all__'
        widgets = {
            'fechaInicioEvaluaciones': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fechaFinEvaluaciones': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

# form for direcciones
class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = '__all__'

# form for gerencias


class GerenciaForm(forms.ModelForm):
    class Meta:
        model = Gerencia
        fields = '__all__'


class EvaluacionForm(forms.ModelForm):
    class Meta:
        model = Evaluacion
        fields = '__all__'


class ObjectivesForm(forms.ModelForm):
    class Meta:
        model = Objetivos
        fields = ['texto', 'tipo']
        widgets = {
            'texto': forms.Textarea(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
        }

class DistribucionObjetivoForm(forms.ModelForm):
    class Meta:
        model = DistribucionObjetivo
        fields = ['tipo', 'peso']
        widgets = {
            'tipo': forms.TextInput(attrs={'class': 'form-control'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'step': '5', 'value': '0'}),
        }

                
        








class ActivitiesForm(forms.ModelForm):
    class Meta:
        model = Actividades
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={'class': 'form-control'}),
        }


class EvaluacionDesempenoForm(forms.ModelForm):
    class Meta:
        model = EvaluacionDesempeno
        fields = ['periodo', 'empleado','estado']

# form for competencias


class CompetenciasForm(forms.ModelForm):
    class Meta:
        model = Competencias
        fields = ['nombre', 'nivel', 'descripcion','significado1', 'significado2', 'significado3', 'significado4']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'nivel': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'significado1': forms.Textarea(attrs={'class': 'form-control'}),
            'significado2': forms.Textarea(attrs={'class': 'form-control'}),
            'significado3': forms.Textarea(attrs={'class': 'form-control'}),
            'significado4': forms.Textarea(attrs={'class': 'form-control'}),
            
        }


class ObjetivosEvaluacionForm(forms.ModelForm):
    objetivo = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'name': 'objetivo'}))
    comentarios = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'name': 'comentarios'}),
        required=False)

    peso = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={'class': 'form-control', 'step': '5', 'value': '0'}),
        min_value=5, max_value=80, required=True, )
    valor = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'value': '0'}),
        min_value=1, max_value=4, required=True)
    resultado = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'value': '0.00'}),
        min_value=0, max_value=4, required=True)

    class Meta:
        model = EvaluacionObjetivo
        fields = ['objetivo', 'peso', 'valor', 'resultado', 'comentarios']

    def __init__(self, *args, **kwargs):
        super(ObjetivosEvaluacionForm, self).__init__(*args, **kwargs)
        try:
            self.initial['objetivo'] = self.instance.objetivo.texto
        except:
            pass


class ActividadesObjetivosEvaluacionForm(forms.ModelForm):
    actividad = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '1', 'name': 'actividad'}))

    class Meta:
        model = ObjetivoActividad
        fields = ['actividad', 'pesoActividad']

    def __init__(self, *args, **kwargs):
        super(ActividadesObjetivosEvaluacionForm,
              self).__init__(*args, **kwargs)
        try:
            self.initial['actividad'] = self.instance.actividad.texto
        except:
            pass


class CompetenciasEvaluacionForm(forms.ModelForm):
    pesoCompetencia = forms.IntegerField(
        min_value=1, max_value=4, required=True, initial=0
    )

    class Meta:
        model = EvaluacionCompetencia
        fields = ['competencia', 'pesoCompetencia', 'resultadoCompetencia']
        widgets = {
            'resultadoCompetencia': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, nivel=None, *args, **kwargs):
        super(CompetenciasEvaluacionForm, self).__init__(*args, **kwargs)
        if nivel:
            self.fields['competencia'].queryset = Competencias.objects.filter(
                nivel=nivel)

# class form for cargo


class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = '__all__'
