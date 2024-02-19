from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from simple_history.models import HistoricalRecords


# Create your models here.

class Nivel(models.Model):
    nivel = models.TextField()
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['nivel']
        verbose_name = 'Clasificación de Nivel'
        verbose_name_plural = 'Clasificación de Niveles'
        
        

    def __str__(self) -> str:
        return self.nivel

    def competencias(self):
        return self.competencias_set.all()


class Niveles(models.Model):
    CHOICES = (
        (0, 'VIP'),
        (1, 'GERENTE DE PRIMERA LINEA'),
        (2, 'GERENTE DE SEGUNDA LINEA'),
        (3, 'JEFE'),
        (4, 'COORDINADOR'),
        (5, 'ASESOR DE NEGOCIOS'),
        (6, 'ESPECIALISTA'),
        (7, 'ANALISTA'),
        (8, 'TECNICO O INSPECTOR'),
        (9, 'ASESOR DE FARMACIA'),
        (10, 'ASISTENTE'),
        (11, 'OPERARIO'),
        (12, 'AUXILIAR')
    )
    formatos = (
        ('pns', 'Personal de Nomina Semanal'),
        ('pnm', 'Personal de Nomina Mensual')              
        )

    valor = models.IntegerField(choices=CHOICES)
    porCompetencias = models.IntegerField(default=50)
    cantidadCompetencias = models.IntegerField(default=2)
    cantidadObjetivos = models.IntegerField(default=4)
    porObjetivos = models.IntegerField(default=50)
    nivel = models.ForeignKey(Nivel, on_delete=models.CASCADE, default=1)
    formato_de_evaluacion = models.TextField(choices=formatos, default='pnm')
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['valor']
        verbose_name = 'Nivel de Cargo'
        verbose_name_plural = 'Niveles de Cargos'

    def __str__(self):
        return f'Nivel {self.valor} - {self.get_choice_value()}'
    
    def get_choice_value(self):
        return dict(self.CHOICES)[self.valor]
    
    def get_formato_de_evaluacion(self):
        return dict(self.formatos)[self.formato_de_evaluacion]
        
        

    def cargos(self):
        return self.cargo_set.all()
    
    def cantidad_cargos(self):
        return self.cargo_set.all().count()
    
    def cantidad_empleados(self):
        suma = 0
        for cargo in self.cargos():
            suma += cargo.empleado_set.filter(fechaEgreso__isnull=True).count()
        return suma

class Direccion(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    debajo = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['id']
        verbose_name = 'Dirección'
        verbose_name_plural = 'Direcciones'
    

    def __str__(self):
        return self.nombre
    
    def subdirecciones(self):
        return self.direccion_set.all()

    def gerencias(self):
        return self.gerencia_set.all()
    
    def empleados_asociados(self):
        return Empleado.objects.filter(cargo__gerencia__direccion=self, fechaEgreso__isnull=True).order_by('cargo__nivel__valor')

    
class Departamento(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['id']
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        
    def get_empleados(self):
        return Empleado.objects.filter(cargo__gerencia__departamento=self, fechaEgreso__isnull=True)
    
    def get_amount_objetivos_generales(self):
        return Objetivos.objects.filter(empleado__cargo__gerencia__departamento=self, periodo=Periodo.objects.get(is_active=True)).count()
    
    def get_amount_objetivos_especificos(self):
        return Actividades.objects.filter(objetivo__empleado__cargo__gerencia__departamento=self, objetivo__periodo=Periodo.objects.get(is_active=True)).count()
    
    def __str__(self):
        return self.nombre
    
    

class Gerencia(models.Model):
    nombreText = models.CharField(max_length=200)    
    direccion = models.ForeignKey(
        Direccion, on_delete=models.SET_NULL, null=True)
    departamento = models.ForeignKey(
        Departamento, on_delete=models.SET_NULL, null=True)
    debajo = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)
    
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['id']
        verbose_name = 'Gerencia'
        verbose_name_plural = 'Gerencias'
    

    def __str__(self):
        return f'Gerencia de {self.nombreText}'
    
    def subgerencias(self):
        return self.gerencia_set.all()

    def cargosAsociados(self):
        return self.cargo_set.all().order_by('nivel__valor')
    
    def empleados_asociados(self):
        return Empleado.objects.filter(cargo__gerencia=self, fechaEgreso__isnull=True).order_by('cargo__nivel__valor')

    def cantidadEmpleados(self):
        cargos = self.cargo_set.all()
        cantidad = 0

        for cargo in cargos:
            cantidad += cargo.empleadosAsociados().count()
        return cantidad

    def objetivosGerencia(self):
        periodo = Periodo.objects.last()
        empleados = Empleado.objects.filter(
            cargo__gerencia=self, fechaEgreso__isnull=True)
        cantidad = 0

        for empleado in empleados:
            cantidad += empleado.objetivos_set.filter(periodo=periodo).count()
        return cantidad

    def porcentajeCompletacionObjetivos(self):
        empleados = Empleado.objects.filter(
            cargo__gerencia=self, fechaEgreso__isnull=True)
        valor = 0

        for empleado in empleados:
            valor += empleado.objetivosPorcentaje()[0]

        return valor/empleados.count()


    
class Distribucion(models.Model):
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    nivel = models.ForeignKey(Niveles, on_delete=models.CASCADE)
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['departamento']
        verbose_name = 'Distribución de Objetivos'
        verbose_name_plural = 'Distribuciones de Objetivos'
    

    def __str__(self):
        return f'{self.departamento} - {self.nivel}'
    
    def distribucionObjetivos(self):
        return self.distribucionobjetivo_set.all()

class DistribucionObjetivo(models.Model):
    distribucion = models.ForeignKey(Distribucion, on_delete=models.CASCADE)
    tipo = models.CharField(default='Objetivo de Area', max_length=200)
    peso = models.IntegerField(default=0)
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['tipo']
        verbose_name = 'Distribución de Objetivo por nivel'
        verbose_name_plural = 'Distribuciones de Objetivos por niveles'

    def __str__(self):
        return f'{self.tipo}({self.peso}%)'



class Cargo(models.Model):
    nombreText = models.CharField(max_length=200)
    supervisor = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)
    nivel = models.ForeignKey(Niveles, on_delete=models.CASCADE, null=True)
    gerencia = models.ForeignKey(Gerencia, on_delete=models.CASCADE, null=True, blank=True)
    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE, null=True, blank=True)
    nombre_infocent = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['nivel', 'nombreText']
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'

    def __str__(self):
        return self.nombreText
    
    def subordinados(self):
        subordinados = list(Cargo.objects.filter(supervisor=self, is_active=True))
        for subordinado in subordinados:
            subordinados.extend(subordinado.subordinados())
        return subordinados
    
    def subordinados_directos(self):
        return Cargo.objects.filter(supervisor=self, is_active=True).order_by('nivel__valor')

    def empleadosAsociados(self):
        return self.empleado_set.all()

    def empleados_activos_asociados(self):
        return self.empleado_set.filter(fechaEgreso__isnull=True).order_by('cargo__nivel__valor')


class Empleado(models.Model):
    imagen = models.ImageField(upload_to='images/', null=True, blank=True)
    nombre = models.TextField(max_length=200)
    apellido = models.TextField(max_length=200)
    cedula = models.IntegerField(default=0, unique=True)
    ficha = models.IntegerField(default=0, unique=True)
    ceco = models.CharField(max_length=15)
    fechaIngreso = models.DateField('Fecha de Ingreso', null=True, blank=True)
    fechaEgreso = models.DateField(null=True, blank=True)
    fechaNacimiento = models.DateField(null=True, blank=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    usuario = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    es_evaluado = models.BooleanField(default=True)
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['ficha']
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'

    # save function that deactivates the usuario if the empleado is given a fechaEgreso 
    def save(self, *args, **kwargs):
        if self.usuario:
            if self.fechaEgreso:
                self.usuario.is_active = False 
                self.usuario.save()
            else:
                self.usuario.is_active = True
                self.usuario.save()

        super(Empleado, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre + ' ' + self.apellido
    
    def get_short_name(self):
        return f'{self.nombre[0]}. {self.apellido.split()[0]}'.title()
    

    def nivel(self):
        return self.cargo.nivel.nivel

    def supervisor(self):
        return Empleado.objects.filter(cargo=self.cargo.supervisor, fechaEgreso__isnull=True).last()
    
    def subordinados(self):  
        cargos = self.cargo.subordinados()
        empleados = Empleado.objects.filter(cargo__in=cargos, fechaEgreso__isnull=True).order_by('cargo__nivel__valor')
        return empleados       
        

    def cantidadEvaluaciones(self):
        return self.evaluaciondesempeno_set.all().exclude(estado=0).count()

    def promedioResultadoFinal(self):
        evaluaciones = self.evaluaciondesempeno_set.exclude(estado=0)
        total_evaluaciones = evaluaciones.count()
        suma_resultados = sum(
            evaluacion.resultadoFinal for evaluacion in evaluaciones)
        if total_evaluaciones > 0:
            promedio = suma_resultados / total_evaluaciones
            return round(promedio, 2)  # Redondear a 2 decimales
        else:
            return 0

    def cantidadObjetivos(self):
        return self.objetivos_set.filter(periodo=Periodo.objects.get(is_active=True)).count()
    
    def cantidadObjetivosTotales(self):
        return self.objetivos_set.all().count()
    
    def cantidad_objetivos_por_estado(self):
        objetivos = self.objetivos_set.filter(periodo=Periodo.objects.get(is_active=True))
        aprobados = 0
        no_aprobados = 0
        completos = 0
        incompletos = 0
        for objetivo in objetivos:
            if objetivo.is_aproved:
                aprobados += 1
            else:
                no_aprobados += 1
            if objetivo.porcentaje() >= 100:
                completos += 1
            else:
                incompletos += 1
        return int(aprobados), int(no_aprobados), int(completos), int(incompletos)

        

    
    def cantidadActividades(self):
        objetivos = self.objetivos_set.filter(periodo=Periodo.objects.get(is_active=True))
        cantidad = 0
        for objetivo in objetivos:
            cantidad += objetivo.actividades_set.all().count()
        return cantidad

    def objetivosPorcentaje(self):
        try:
            objetivo = self.objetivos_set.filter(periodo=Periodo.objects.get(is_active=True))
            valor = 0
            completo = 0
            incompletas = 0
            totalActividades = 0
            totalActividadesCompletas = 0
            cantidad = self.objetivos_set.filter(periodo=Periodo.objects.get(is_active=True)).count()
            for obj in objetivo:
                valor += obj.porcentaje()
                if (obj.porcentaje() >= float(100)):
                    completo += 1
                totalActividades += obj.detallesActividades()[0]
                totalActividadesCompletas += obj.detallesActividades()[1]
            valor /= cantidad
            incompletas = cantidad - completo
            return valor, cantidad, completo, totalActividades, totalActividadesCompletas, incompletas
        except:
            return 0, 0, 0, 0, 0, 0
        
    def distribucionObjetivos(self):
        try:
            nivel = self.cargo.nivel
            departamento = self.cargo.gerencia.departamento
            distribucion = Distribucion.objects.get(nivel=nivel, departamento=departamento)
            return distribucion.distribucionobjetivo_set.all()
        except:
            return None
        
    def distribucionObjetivosCantidad(self):
        distribuciones = self.distribucionObjetivos()

        resultados = []
        for dist in distribuciones:
            resultado = {}
            resultado['tipo'] = dist.tipo 
            resultado['peso'] = dist.peso
            cantidadObjetivos = self.objetivos_set.filter(tipo=dist, periodo=Periodo.objects.get(is_active=True)).count()
            resultado['cantidad'] = cantidadObjetivos
            resultados.append(resultado)

        return resultados

            



    # def distribucionObjetivos(self):
    #     return self.objetivos_set.filter(tipo='OPERATIVO').count(), self.objetivos_set.filter(tipo='ESTRATEGICO').count(), self.objetivos_set.filter(tipo='ADMINISTRATIVO').count()

    def comentariosRecibidos(self):
        return comentarios.objects.filter(para=self).order_by('-fecha')


class Periodo(models.Model):
    año_inicio = models.IntegerField(default=datetime.now().year, unique=True)
    año_fin = models.IntegerField(default=datetime.now().year+1, unique=True)
    fechaInicioEvaluaciones = models.DateField(
        'Fecha de Inicio', null=True, blank=True)
    fechaFinEvaluaciones = models.DateField(
        'Fecha de Fin', null=True, blank=True)
    evaluacionesHabilitadas = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['-año_inicio']
        verbose_name = 'Período'
        verbose_name_plural = 'Períodos'

    def __str__(self):
        return f'Período {self.año_inicio} - {self.año_fin}'
    
    def save(self, *args, **kwargs):
        if self.is_active:
            Periodo.objects.filter(is_active=True).update(is_active=False)
        super(Periodo, self).save(*args, **kwargs)

    def objetivosPeriodo(self):
        return self.objetivos_set.all().count()

    def evaluacionesPeriodo(self):
        return self.evaluaciondesempeno_set.exclude(estado=0).count()

    def promedioEvaluaciones(self):
        evaluaciones = self.evaluaciondesempeno_set.exclude(estado=0)
        total_evaluaciones = evaluaciones.count()
        suma_resultados = sum(
            evaluacion.resultadoFinal for evaluacion in evaluaciones)
        if total_evaluaciones > 0:
            promedio = suma_resultados / total_evaluaciones
            return round(promedio, 2)

    def estado(self):
        try:
            now = datetime.now().date()
            if self.fechaInicioEvaluaciones <= now <= self.fechaFinEvaluaciones and self.evaluacionesHabilitadas:
                return 'En Proceso'
            elif now < self.fechaInicioEvaluaciones:
                return 'No ha comenzado'
            elif now > self.fechaFinEvaluaciones and self.evaluacionesHabilitadas:
                return 'Prorroga'
            else:
                return 'Finalizado'
        except:
            return 'Fechas no definidas'

class Company_Objectives(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    period = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = 'Objetivo de la Empresa'
        verbose_name_plural = 'Objetivos de la Empresa'
    
    def __str__(self):
        return f'{self.period} - {self.title}'
 
 
class Announcements(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = 'Anuncio'
        verbose_name_plural = 'Anuncios'
    
    def __str__(self):
        return self.title

class Objetivos(models.Model):
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    texto = models.TextField()
    tipo = models.ForeignKey(DistribucionObjetivo, on_delete=models.CASCADE, null=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    is_aproved = models.BooleanField(default=False)
    aproved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='aprobado_por', null=True, blank=True)
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['created']
        verbose_name = 'Objetivo General'
        verbose_name_plural = 'Objetivos Generales'

    def __str__(self):
        return str(self.empleado.ficha) + '-' + self.texto

    def porcentaje(self):
        try:
            return float(f'{(self.actividades_set.filter(estado=True).count() * 100) / self.actividades_set.count()}')
        except:
            return float(0)

    def detallesActividades(self):
        actividades = self.actividades_set.count()
        completadas = self.actividades_set.filter(estado=True).count()
        return actividades, completadas

    def actividades(self):
        return self.actividades_set.all()
    
    def notes(self):
        return self.objectives_notes_set.all()
    
    def see_history(self):
        return self.history.all()
    

class Objectives_notes(models.Model):
    objetivo = models.ForeignKey(Objetivos, on_delete=models.CASCADE)
    note = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['created_at']
        verbose_name = 'Nota de Objetivo'
        verbose_name_plural = 'Notas de Objetivos'
    
    def __str__(self):
        return f'{self.objetivo} - {self.note}'

class Actividades(models.Model):
    objetivo = models.ForeignKey(Objetivos, on_delete=models.CASCADE)
    texto = models.TextField()
    estado = models.BooleanField(default=False, blank=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['created']
        verbose_name = 'Objetivo Especifico'
        verbose_name_plural = 'Objetivos Especificos'      

    def __str__(self):
        return self.objetivo.texto + '-' + self.texto


class Competencias(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    nivel = models.ForeignKey(Nivel, on_delete=models.CASCADE)
    significado1 = models.TextField(blank=True, null=True)
    significado2 = models.TextField(blank=True, null=True)
    significado3 = models.TextField(blank=True, null=True)
    significado4 = models.TextField(blank=True, null=True)
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['nivel', 'nombre']
        verbose_name = 'Competencia'
        verbose_name_plural = 'Competencias'

    def __str__(self):
        return f'{self.nivel} - {self.nombre}'



class EvaluacionDesempeno(models.Model):
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    resultadoObjetivos = models.DecimalField(
        max_digits=5, decimal_places=2, default=0)
    resultadoCompetencias = models.DecimalField(
        max_digits=5, decimal_places=2, default=0)
    resultadoFinal = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)
    fecha = models.DateField(auto_now_add=True)
    estado = models.IntegerField(choices=((0, 'Borrador'),
                                          (1, 'Autoevaluacion'),
                                          (2, 'Evaluacion')
                                          ), default=0, null=True, blank=True)
    deteccionCompetencia1 = models.TextField(default="", null=True, blank=True)
    deteccionCompetencia2 = models.TextField(default="", null=True, blank=True)
    deteccionCompetencia3 = models.TextField(default="", null=True, blank=True)
    deteccionTecConductual1 = models.TextField(
        default="", null=True, blank=True)
    deteccionTecConductual2 = models.TextField(
        default="", null=True, blank=True)
    deteccionTecConductual3 = models.TextField(
        default="", null=True, blank=True)
    comentarios = models.TextField(default="", null=True, blank=True)
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Evaluación de Desempeño'
        verbose_name_plural = 'Evaluaciones de Desempeño'

    def __str__(self):
        return f'Evaluación de {self.empleado} - {self.periodo}'

    def save(self):
        self.resultadoFinal = self.resultadoObjetivos + self.resultadoCompetencias
        super().save()

    def validar(self):
        pass


class EvaluacionObjetivo(models.Model):
    evaluacion = models.ForeignKey(
        EvaluacionDesempeno, on_delete=models.CASCADE)
    objetivo = models.ForeignKey(Objetivos, on_delete=models.CASCADE)
    peso = models.IntegerField(default=5)
    valor = models.IntegerField(default=1, validators=[
        MinValueValidator(1), MaxValueValidator(4)])
    resultado = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    comentarios = models.TextField(default="", null=True, blank=True)
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['objetivo']
        verbose_name = 'Evaluación de Objetivo'
        verbose_name_plural = 'Evaluaciones de Objetivos'

    def __str__(self):
        return f'{self.evaluacion} - {self.objetivo}'


class EvaluacionCompetencia(models.Model):
    Evaluacion = models.ForeignKey(
        EvaluacionDesempeno, on_delete=models.CASCADE)
    competencia = models.ForeignKey(
        Competencias, on_delete=models.CASCADE, null=True)
    pesoCompetencia = models.PositiveIntegerField(default=1, validators=[
        MaxValueValidator(4), MinValueValidator(1)],
        help_text='Ingrese un valor entre 1 y 4.'
    )
    resultadoCompetencia = models.DecimalField(
        default=0, decimal_places=2, max_digits=5)
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['competencia']
        verbose_name = 'Evaluación de Competencia'
        verbose_name_plural = 'Evaluaciones de Competencias'
        
    def __str__(self):
        return f'{self.Evaluacion} - {self.competencia}'


class ObjetivoActividad(models.Model):
    objetivo = models.ForeignKey(EvaluacionObjetivo, on_delete=models.CASCADE)
    actividad = models.ForeignKey(Actividades, on_delete=models.CASCADE)
    pesoActividad = models.IntegerField(default=0)
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['actividad']
        verbose_name = 'Peso Objetivo Especifico'
        verbose_name_plural = 'Pesos Objetivos Especificos'

    def __str__(self):
        return self.actividad.texto
        # return f'{self.objetivo.evaluacion} - {self.objetivo.objetivo} - {self.actividad}'


class comentarios(models.Model):
    de = models.ForeignKey(
        Empleado, on_delete=models.CASCADE, related_name='emisor')
    para = models.ForeignKey(
        Empleado, on_delete=models.CASCADE, related_name='receptor')
    comentario = models.TextField(default="")
    fecha = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'

    def __str__(self):
        return f'{self.de} - {self.comentario}'

class Preguntas_Frecuentes(models.Model):
    pregunta = models.TextField()
    respuesta = models.TextField()
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = 'Pregunta Frecuente'
        verbose_name_plural = 'Preguntas Frecuentes'
        
    def __str__(self):
        return self.pregunta
    
class Factores_de_evaluacion_PNS(models.Model):
    nombre = models.TextField()
    enfoque = models.CharField(max_length=200, choices=(
        ('Buenas practicas operativas', 'Buenas Practicas Operativas'),
        ('Procesos', 'Procesos'),
        ('Seguridad y salud laboral', 'Seguridad y Salud Laboral'),
        ('Competencias actidudinales', 'Competencias Actitudinales')        
    ), default='Buenas practicas operativas')
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['enfoque', 'nombre']
        verbose_name = 'Factor de Evaluación PNS'
        verbose_name_plural = 'Factores de Evaluación PNS'
    
    def __str__(self):
        return f'{self.enfoque} - {self.nombre}'
    
class Evaluacion_PNS(models.Model):
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    resultado = models.IntegerField(default=0)
    fecha = models.DateField(auto_now_add=True)
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Evaluación PNS'
        verbose_name_plural = 'Evaluaciones PNS'
    
    def __str__(self):
        return f'Evaluacion de {self.empleado.nombre} {self.empleado.apellido} - {self.periodo}'
    
    def factores(self):
        return self.evaluacion_pns_bpo_set.all()
    
    def calcular_resultado(self):
        factores = self.factores()
        resultado = 0
        for factor in factores:
            resultado += factor.valor
        self.resultado = resultado
        self.save()
        
    
class Evaluacion_PNS_BPO(models.Model):
    evaluacion = models.ForeignKey(Evaluacion_PNS, on_delete=models.CASCADE)
    factor = models.ForeignKey(Factores_de_evaluacion_PNS, on_delete=models.CASCADE)
    valor = models.IntegerField(default=0, validators=[
        MinValueValidator(1), MaxValueValidator(3)])
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['factor']
        verbose_name = 'Evaluación BPO'
        verbose_name_plural = 'Evaluaciones BPO'
    
    def __str__(self):
        return f'{self.evaluacion} - {self.factor}'
