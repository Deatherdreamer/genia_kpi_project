from django.contrib import admin
from .models import *
from simple_history.admin import SimpleHistoryAdmin

admin.site.site_title = "Genia Performance 360 Pro"
admin.site.site_header = "Genia Performance 360 Pro"
admin.site.index_title = "Panel de Administración Genia Performance 360 Pro"

@admin.register(Empleado)
class EmpleadoAdmin(SimpleHistoryAdmin):
    search_fields = ('ficha', 'nombre', 'apellido')
    list_display = ('ficha', 'nombre', 'apellido')



admin.site.register(Cargo)
admin.site.register(Gerencia)
admin.site.register(Niveles)
admin.site.register(Direccion)
admin.site.register(Competencias)
admin.site.register(Evaluacion)
admin.site.register(Periodo)
admin.site.register(Objetivos)
admin.site.register(Actividades)
admin.site.register(EvaluacionDesempeno)
admin.site.register(EvaluacionObjetivo)
admin.site.register(ObjetivoActividad)
admin.site.register(EvaluacionCompetencia)
admin.site.register(Nivel)
admin.site.register(comentarios)
admin.site.register(Departamento)
admin.site.register(Distribucion)
admin.site.register(DistribucionObjetivo)
admin.site.register(Preguntas_Frecuentes)
admin.site.register(Factores_de_evaluacion_PNS)
admin.site.register(Evaluacion_PNS)
admin.site.register(Evaluacion_PNS_BPO)
admin.site.register(Announcements)
admin.site.register(Company_Objectives)
admin.site.register(Objectives_notes)
