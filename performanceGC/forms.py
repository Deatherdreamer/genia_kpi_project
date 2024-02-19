from django import forms
import datetime
from django.forms import TextInput
from .models import *


class EmpleadoForm(forms.ModelForm):
    fechaIngreso = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'))
    fechaNacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
        required=False
    )
    
    
    class Meta:
        model = Empleado
        exclude = ['fechaEgreso', 'usuario']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput( attrs={'class': 'form-control'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'ficha': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo': forms.Select(attrs={'class': 'form-select'}),
            'ceco': forms.TextInput(attrs={'class': 'form-control'}),
            
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

        
class ObjectivesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.empleado = kwargs.pop('empleado', None)
        super(ObjectivesForm, self).__init__(*args, **kwargs)
        if self.empleado is not None:
            self.fields['tipo'].queryset = self.empleado.distribucionObjetivos()

    class Meta:
        model = Objetivos
        fields = ['texto', 'tipo']
        widgets = {
            'texto': forms.Textarea(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'texto': 'Descripción del objetivo',
            'tipo': 'Tipo de objetivo',
        }
        help_texts = {
            'texto': 'Texto descriptivo del objetivo a cumplir.',
            'tipo': 'Seleccione el tipo de objetivo que desea agregar.',
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
            'texto': forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}),
        }
        labels = {
            'texto': 'Descripción del objetivo específico',
        }
        help_texts = {
            'texto': 'Texto descriptivo del objetivo específico para el objetivo general seleccionado.',
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
            'descripcion': forms.Textarea(attrs={'class': 'form-control','rows':'4'}),
            'significado2': forms.Textarea(attrs={'class': 'form-control', 'rows':'4'}),
            'significado3': forms.Textarea(attrs={'class': 'form-control', 'rows':'4'}),
            'significado4': forms.Textarea(attrs={'class': 'form-control', 'rows':'4'}),            
            'significado1': forms.Textarea(attrs={'class': 'form-control', 'rows':'4'}),
        }
        labels = {
            'nombre': 'Nombre de la Competencia',
            'nivel': 'Nivel de la Competencia',
            'descripcion': 'Descripción de la Competencia',
            'significado1': '1 - No hay dominio',
            'significado2': '2 - Dominio Básico',
            'significado3': '3 - Dominio Parcial',
            'significado4': '4 - Dominio Superior',
        }
        help_texts = {
            'nombre': 'Nombre de la competencia.',
            'nivel': 'Nivel de la competencia.',
            'descripcion': 'Descripción detallada del significado de la competencia.',
            'significado1': 'Significado al indicar resultado 1.',
            'significado2': 'Significado al indicar resultado 2.',
            'significado3': 'Significado al indicar resultado 3.',
            'significado4': 'Significado al indicar resultado 4.',
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
        fields = ['nombreText','nombre_infocent', 'supervisor', 'nivel', 'gerencia', 'direccion']
        widgets = {
            'nombreText': forms.TextInput(attrs={'class': 'form-control'}),
            'supervisor': forms.Select(attrs={'class': 'form-select'}),            
            'nivel': forms.Select(attrs={'class': 'form-select'}),
            'gerencia': forms.Select(attrs={'class': 'form-select'}),
            'direccion': forms.Select(attrs={'class': 'form-select'}),
            'nombre_infocent': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nombreText': 'Nombre del Cargo',
            'supervisor': 'Cargo Supervisor',
            'nivel': 'Nivel',
            'gerencia': 'Gerencia',
            'direccion': 'Direccion',
            'nombre_infocent': 'Nombre en Infocent',
            'is_active': 'Activo',
        }
        help_texts = {
            'nombreText': 'Nombre del cargo para el sistema.',
            'nombre_infocent': 'Nombre que tiene el cargo en Infocent.',
            'supervisor': 'Cargo que supervisa este cargo.',
            'nivel': 'Nivel del cargo.',
            'gerencia': 'Gerencia a la que pertenece el cargo.',
            'direccion': 'Direccion a la que pertenece el cargo.',
            'is_active': 'Si el cargo esta Activo o inactivo.',            
        }


#class form for announcements
class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcements
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Encabezado',
            'text': 'Mensaje del anuncio',
            'image': 'Imagen',
        }
        help_texts = {
            'title': 'Titulo del anuncio.',
            'text': 'Texto del anuncio.',
            'image': 'Imagen del anuncio.',
        }
        
class CompanyObjectivesForm(forms.ModelForm):
    class Meta:
        model = Company_Objectives
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Titulo',
            'description': 'Descripcion',
        }
        
class ObjectivesNotesForm(forms.ModelForm):
    class Meta:
        model = Objectives_notes
        fields = ['note']
        widgets = {
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'})
        }
        labels = {
            'note': 'Texto de la Nota',
        }
