from django import forms
import datetime
from django.forms import TextInput
from .models import *


class EmpleadoForm(forms.ModelForm):
    fechaIngreso = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
        required=True,
        label='Fecha de Ingreso',
        help_text='Fecha de ingreso del empleado.',        
        )

    fechaNacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
        required=False,
        label='Fecha de Nacimiento',
        help_text='Fecha de nacimiento del empleado.',
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
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),      
        }
        labels = {
            'nombre': 'Nombres',
            'apellido': 'Apellidos',
            'cedula': 'Cedula',
            'ficha': 'Ficha',
            'cargo': 'Cargo',
            'ceco': 'CECO',
            'imagen': 'Fotografía de Perfil',
        }
        help_texts = {
            'nombre': 'Nombres del empleado.',
            'apellido': 'Apellidos del empleado.',
            'cedula': 'Cedula del empleado.',
            'ficha': 'Ficha del empleado.',
            'cargo': 'Cargo del empleado.',
            'ceco': 'CECO del empleado.',
            'imagen': 'Fotografía del empleado.',
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
        labels = {
            'año_inicio': 'Año Inicio del Periodo',
            'año_fin': 'Año de Cierre del Periodo',
            'fechaInicioEvaluaciones': 'Fecha de Inicio del Proceso de Evaluacion',
            'fechaFinEvaluaciones': 'Fecha de Cierre del Proceso de Evaluacion',
            'evaluacionesHabilitadas': 'Activar/Desactivar Proceso de Evaluacion',
            'is_active': 'Activar/Desactivar Periodo (Solo puede haber un periodo activo al mismo tiempo.)'
        }
            
            
        

# form for direcciones
class DireccionForm(forms.ModelForm):
    '''
    nombre = models.CharField(max_length=200, unique=True)
    debajo = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)
    '''
    class Meta:
        model = Direccion
        fields = ['nombre', 'debajo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'debajo': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'nombre': 'Nombre de la Dirección',
            'debajo': 'Dirección Superior',
        }
        help_texts = {
            'nombre': 'Nombre de la dirección. Solo coloque el nombre, no incluya la palabra "Dirección".',
            'debajo': 'Dirección superior a la que pertenece la dirección.',
        }
        
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        qs = Direccion.objects.filter(nombre=nombre)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Ya existe una dirección con este nombre.')
        return nombre
    

# form for gerencias
class GerenciaForm(forms.ModelForm):
    '''
    nombreText = models.CharField(max_length=200)    
    direccion = models.ForeignKey(
        Direccion, on_delete=models.SET_NULL, null=True)
    departamento = models.ForeignKey(
        Departamento, on_delete=models.SET_NULL, null=True)
    debajo = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)
        '''
    class Meta:
        model = Gerencia
        fields = ['nombreText', 'direccion', 'departamento', 'debajo']
        widgets = {
            'nombreText': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Select(attrs={'class': 'form-select'}),
            'departamento': forms.Select(attrs={'class': 'form-select'}),
            'debajo': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'nombreText': 'Nombre de la Gerencia',
            'direccion': 'Dirección a la que pertenece',
            'departamento': 'Departamento',
            'debajo': 'Gerencia Superior',
        }
        help_texts = {
            'nombreText': 'Nombre de la gerencia. Solo coloque el nombre, no incluya la palabra "Gerencia".',
            'direccion': 'Dirección a la que pertenece la gerencia.',
            'departamento': 'Departamento al que pertenece la gerencia.',
            'debajo': 'Gerencia superior a la que pertenece la gerencia.',
        }
    
    def clean_nombreText(self):
        nombreText = self.cleaned_data['nombreText']
        qs = Gerencia.objects.filter(nombreText=nombreText)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Ya existe una gerencia con este nombre.')
        return nombreText

    
            

        
class ObjectivesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.empleado = kwargs.pop('empleado', None)
        super(ObjectivesForm, self).__init__(*args, **kwargs)
        if self.empleado is not None:
            self.fields['tipo'].queryset = self.empleado.distribucionObjetivos()

    class Meta:
        model = Objetivos
        fields = ['tipo','texto']
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
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5', 'name': 'objetivo'}))
    comentarios = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5', 'name': 'comentarios'}),
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
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5', 'name': 'actividad'}))

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
    
    def clean_nombreText(self):
        nombreText = self.cleaned_data['nombreText']
        if self.instance.pk:
            # Editing an existing Cargo
            if Cargo.objects.filter(nombreText=nombreText).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('Ya existe un cargo con este nombre.')
        else:
            # Creating a new Cargo
            if Cargo.objects.filter(nombreText=nombreText).exists():
                raise forms.ValidationError('Ya existe un cargo con este nombre.')
        return nombreText
    


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
