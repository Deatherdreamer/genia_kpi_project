from django.contrib import admin
from .models import *
from simple_history.admin import SimpleHistoryAdmin

admin.site.site_title = "Genia Performance 360 Pro"
admin.site.site_header = "Genia Performance 360 Pro"
admin.site.index_title = "Panel de Administración Genia Performance 360 Pro"

@admin.register(Nivel)
class NivelAdmin(SimpleHistoryAdmin):
    search_fields = ('nivel',)
    list_display = ('nivel',)
    
@admin.register(Niveles)
class NivelesAdmin(SimpleHistoryAdmin):
    search_fields = ('valor','nivel')
    list_display =  ('valor','nivel')

    
@admin.register(Direccion)
class DireccionAdmin(SimpleHistoryAdmin):
    search_fields = ('nombre',)
    list_display = ('nombre',)
    
@admin.register(Departamento)
class DepartamentoAdmin(SimpleHistoryAdmin):
    search_fields = ('nombre',)
    list_display = ('nombre',)
    
@admin.register(Gerencia)
class GerenciaAdmin(SimpleHistoryAdmin):
    search_fields = ('nombreText', 'direccion', 'departamento' )
    list_display = ('nombreText', 'direccion', 'departamento' )
    
@admin.register(Distribucion)
class DistribucionAdmin(SimpleHistoryAdmin):
    search_fields = ('nivel','departamento')
    list_display = ('nivel','departamento')

@admin.register(DistribucionObjetivo)
class DistribucionObjetivoAdmin(SimpleHistoryAdmin):
    search_fields = ('tipo','peso','distribucion')
    list_display = ('tipo','peso','distribucion')

@admin.register(Cargo)
class CargoAdmin(SimpleHistoryAdmin):
    search_fields = ('nombreText','supervisor','gerencia','direccion','nivel',)
    list_display = ('nombreText','supervisor','gerencia','direccion','nivel',)

@admin.register(Empleado)
class EmpleadoAdmin(SimpleHistoryAdmin):
    search_fields = ('ficha', 'nombre', 'apellido', 'cargo')
    list_display = ('ficha', 'nombre', 'apellido', 'cargo')
    
@admin.register(Periodo)
class PeriodoAdmin(SimpleHistoryAdmin):
    search_fields = ('año_inicio','año_fin','is_active',)
    list_display = ('año_inicio','año_fin','is_active',)
    
@admin.register(Company_Objectives)
class Company_ObjectivesAdmin(SimpleHistoryAdmin):
    search_fields = ('title','description','period', )
    list_display = ('title','description','period', )
    
@admin.register(Announcements)
class AnnouncementsAdmin(SimpleHistoryAdmin):
    search_fields = ('title','text','date', )
    list_display = ('title','text','date', )
    
@admin.register(Objetivos)
class ObjetivosAdmin(SimpleHistoryAdmin):
    search_fields = ('texto','empleado','tipo','periodo', )
    list_display = ('texto','empleado','tipo','periodo', )
    
@admin.register(Objectives_notes)
class Objectives_notesAdmin(SimpleHistoryAdmin):
    search_fields = ('note','objetivo' )
    list_display = ('note','objetivo' )
    
@admin.register(Actividades)
class ActividadesAdmin(SimpleHistoryAdmin):
    search_fields = ('texto','objetivo','estado', )
    list_display = ('texto','objetivo','estado', )
    
@admin.register(Competencias)
class CompetenciasAdmin(SimpleHistoryAdmin):
    search_fields = ('nombre','descripcion', )
    list_display = ('nombre','descripcion', )
    
@admin.register(comentarios)
class comentariosAdmin(SimpleHistoryAdmin):
    search_fields = ('comentario','de','fecha', )
    list_display = ('comentario','de','fecha', )
    
@admin.register(Preguntas_Frecuentes)
class Preguntas_FrecuentesAdmin(SimpleHistoryAdmin):
    search_fields = ('pregunta','respuesta', )
    list_display = ('pregunta','respuesta', )
    

