from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class Nivel(models.Model):
    nivel = models.TextField()

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
    

    def __str__(self):
        return self.nombre

    def gerencias(self):
        return self.gerencia_set.all()

    
class Departamento(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    
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
    

    def __str__(self):
        return f'Gerencia de {self.nombreText}'

    def cargosAsociados(self):
        return self.cargo_set.all().order_by('nivel__valor')

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

    def __str__(self):
        return f'{self.departamento} - {self.nivel}'
    
    def distribucionObjetivos(self):
        return self.distribucionobjetivo_set.all()

class DistribucionObjetivo(models.Model):
    distribucion = models.ForeignKey(Distribucion, on_delete=models.CASCADE)
    tipo = models.CharField(default='Objetivo de Area', max_length=200)
    peso = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.tipo}({self.peso}%)'



class Cargo(models.Model):
    nombreText = models.CharField(max_length=200)
    supervisor = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)
    nivel = models.ForeignKey(Niveles, on_delete=models.CASCADE, null=True)
    gerencia = models.ForeignKey(Gerencia, on_delete=models.CASCADE, null=True, blank=True)
    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombreText

    def empleadosAsociados(self):
        return self.empleado_set.all()


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
        cargos_subordinados = Cargo.objects.filter(supervisor=self.cargo)
        empleados_subordinados = Empleado.objects.filter(
            cargo__in=cargos_subordinados).exclude(fechaEgreso__isnull=False)
        subordinados = list(empleados_subordinados)
        for empleado in empleados_subordinados:
            subordinados.extend(empleado.subordinados())
        return subordinados

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
        return self.objetivos_set.filter(periodo=Periodo.objects.last()).count()
    
    def cantidadObjetivosTotales(self):
        return self.objetivos_set.all().count()
    
    def cantidadActividades(self):
        objetivos = self.objetivos_set.all()
        cantidad = 0
        for objetivo in objetivos:
            cantidad += objetivo.actividades_set.all().count()
        return cantidad

    def objetivosPorcentaje(self):
        try:
            objetivo = self.objetivos_set.all()
            valor = 0
            completo = 0
            incompletas = 0
            totalActividades = 0
            totalActividadesCompletas = 0
            for obj in objetivo:
                valor += obj.porcentaje()
                if (obj.porcentaje() >= float(100)):
                    completo += 1
                totalActividades += obj.detallesActividades()[0]
                totalActividadesCompletas += obj.detallesActividades()[1]
            valor /= self.objetivos_set.count()
            incompletas = self.objetivos_set.count() - completo
            return valor, self.objetivos_set.count(), completo, totalActividades, totalActividadesCompletas, incompletas
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
            cantidadObjetivos = self.objetivos_set.filter(tipo=dist).count()
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

    def __str__(self):
        return f'Periodo {self.año_inicio} - {self.año_fin}'

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


class Objetivos(models.Model):
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    texto = models.TextField()
    tipo = models.ForeignKey(DistribucionObjetivo, on_delete=models.CASCADE, null=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

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


class Actividades(models.Model):
    objetivo = models.ForeignKey(Objetivos, on_delete=models.CASCADE)
    texto = models.TextField()
    estado = models.BooleanField(default=False, blank=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

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

    def __str__(self):
        return f'{self.nivel} - {self.nombre}'


# class ValoresCompetencias(models.Model):
#     competencia = models.ForeignKey(Competencias, on_delete=models.CASCADE)
#     valor = models.IntegerField(default=1, validators=[
#         MinValueValidator(1), MaxValueValidator(4)])
#     significado = models.TextField()

#     def __str__(self):
#         return f'{self.competencia} - {self.valor}'


class Evaluacion(models.Model):

    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    estado = models.IntegerField(choices=((0, 'Autoevaluacion'),
                                 (1, 'Evaluacion')), default=0, null=True, blank=True)
    obj1 = models.TextField(default="")
    peso1 = models.IntegerField(default=0)
    valor1 = models.IntegerField(default=0, validators=[
                                 MinValueValidator(1), MaxValueValidator(4)])
    resultado1 = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    observaciones1 = models.TextField(default="")

    obj2 = models.TextField(default="")
    peso2 = models.IntegerField(default=0)
    valor2 = models.IntegerField(default=0, validators=[
                                 MinValueValidator(1), MaxValueValidator(4)])
    resultado2 = models.DecimalField(
        default=0, max_digits=5, decimal_places=2, null=True, blank=True)
    observaciones2 = models.TextField(default="")

    obj3 = models.TextField(default="")
    peso3 = models.IntegerField(default=0)
    valor3 = models.IntegerField(default=0, validators=[
                                 MinValueValidator(1), MaxValueValidator(4)])
    resultado3 = models.DecimalField(
        default=0, max_digits=5, decimal_places=2, null=True, blank=True)
    observaciones3 = models.TextField(default="")

    obj4 = models.TextField(null=True, blank=True)
    peso4 = models.IntegerField(default=0, null=True, blank=True)
    valor4 = models.IntegerField(default=0, validators=[
                                 MinValueValidator(1), MaxValueValidator(4)], null=True, blank=True)
    resultado4 = models.DecimalField(
        default=0, max_digits=5, decimal_places=2, null=True, blank=True)
    observaciones4 = models.TextField(null=True, blank=True)

    totalObj = models.DecimalField(
        default=0, max_digits=5, decimal_places=2, null=True, blank=True)

    com1 = models.TextField(default="")
    comv1 = models.IntegerField(default=0, validators=[
        MinValueValidator(1), MaxValueValidator(4)])
    comr1 = models.DecimalField(
        default=0, max_digits=5, decimal_places=2, null=True, blank=True)

    com2 = models.TextField(default="")
    comv2 = models.IntegerField(default=0, validators=[
        MinValueValidator(1), MaxValueValidator(4)])
    comr2 = models.DecimalField(
        default=0, max_digits=5, decimal_places=2, null=True, blank=True)

    com3 = models.TextField(null=True, blank=True)
    comv3 = models.IntegerField(default=0, validators=[
        MinValueValidator(1), MaxValueValidator(4)], null=True, blank=True)
    comr3 = models.DecimalField(
        default=0, max_digits=5, decimal_places=2, null=True, blank=True)

    totalCom = models.DecimalField(
        default=0, max_digits=5, decimal_places=2, null=True, blank=True)

    nCom1 = models.TextField(null=True, blank=True)
    nCom2 = models.TextField(null=True, blank=True)
    nCom3 = models.TextField(null=True, blank=True)

    nComR1 = models.TextField(null=True, blank=True)
    nComR2 = models.TextField(null=True, blank=True)
    nComR3 = models.TextField(null=True, blank=True)

    comentarios = models.TextField(null=True, blank=True)

    def validar(self):
        print(int(self.peso1))
        print(int(self.peso2))
        print(int(self.peso3))
        return (self.empleado.cargo.nivel.porObjetivos == int(self.peso1) + int(self.peso2) + int(self.peso3) + int(self.peso4))

    def resultadoTotal(self):
        return self.totalCom + self.totalObj

    def __str__(self):
        return "Evaluacion de " + self.empleado.nombre + " " + self.empleado.nombre


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


class ObjetivoActividad(models.Model):
    objetivo = models.ForeignKey(EvaluacionObjetivo, on_delete=models.CASCADE)
    actividad = models.ForeignKey(Actividades, on_delete=models.CASCADE)

    pesoActividad = models.IntegerField(default=0)

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

    def __str__(self):
        return f'{self.de} - {self.comentario}'

class Preguntas_Frecuentes(models.Model):
    pregunta = models.TextField()
    respuesta = models.TextField()
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
    
    def __str__(self):
        return f'{self.enfoque} - {self.nombre}'
    
class Evaluacion_PNS(models.Model):
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    resultado = models.IntegerField(default=0)
    fecha = models.DateField(auto_now_add=True)
    
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
    
    def __str__(self):
        return f'{self.evaluacion} - {self.factor}'

    