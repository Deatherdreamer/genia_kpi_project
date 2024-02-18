
import os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required 
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Q
from django.db import transaction
from .models import *
from .forms import *
from django.template.loader import get_template
from xhtml2pdf import pisa
from openpyxl import Workbook
import pandas as pd    
from django.views.generic import ListView
from django.contrib import messages


def index(request):
    return render(request, 'index.html')

# def debugTests(request):
#     competencias = Competencias.objects.all()
#     return render(request, 'cosasraras.html',
#                   {'competencias': competencias})

@staff_member_required
def createUser(request):
    empleados = Empleado.objects.all().filter(fechaEgreso__isnull=True).filter(
        usuario__isnull=True).order_by('cargo__nivel__valor')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            empleado = get_object_or_404(
                Empleado, ficha=request.POST['empleado'])
            user = form.save(commit=False)
            user.save()
            empleado.usuario = user
            empleado.save()

            return redirect('profile', e_ficha=request.user.empleado.ficha)
    else:
        form = UserCreationForm()
    return render(request, 'createUser.html', {'form': form, 'empleados': empleados})

@staff_member_required
def users(request):
    users = User.objects.all().order_by('-is_superuser', '-is_staff',
                                        'empleado__cargo__nivel__valor')
    return render(request, 'users.html', {'users': users})

@login_required
def masterEmployee(request):
    if request.user.is_staff:
        empleados = Empleado.objects.all().order_by(
            'cargo__nivel__valor').exclude(fechaEgreso__isnull=False)
    else:
        usuario = request.user
        print(usuario)
        empleado = usuario.empleado
        print(empleado)
        empleados = empleado.subordinados().exclude(fechaEgreso__isnull=False)

    return render(request, 'master.html', {
        'empleados': empleados
    })
            
    # # q = request.GET.get('q') if request.GET.get('q') != None else ''
    # q = request.GET.get('q', '')

    # empleado = Empleado.objects.filter(
    #     Q(nombre__icontains=q) |
    #     Q(apellido__icontains=q) |
    #     Q(ficha__icontains=q) |
    #     Q(cedula__icontains=q) |
    #     Q(ceco__icontains=q) |
    #     Q(cargo__nombreText__icontains=q) |
    #     Q(cargo__gerencia__nombreText__icontains=q)
    # ).order_by('cargo__nivel__valor').exclude(fechaEgreso__isnull=False)
    # return render(request, 'master.html', {
    #     'empleados': empleado
    # })

@login_required
def profileView(request, e_ficha):   
    empleado = get_object_or_404(Empleado, ficha=e_ficha)
    cargo = empleado.cargo   
    evaluaciones = EvaluacionDesempeno.objects.filter(empleado=empleado)
    periodo = Periodo.objects.get(is_active=True)

    return render(request, 'profile.html', {
        'empleado': empleado,
        'cargo': cargo,
        'evaluaciones': evaluaciones,
        'periodo': periodo
    })

@staff_member_required(login_url='signin')
def addEmployee(request):
    if request.method == 'GET':
        return render(request, 'addEmployee.html', {
            'form': EmpleadoForm()
        })
    else:
        form = EmpleadoForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                empleado = form.save(commit=False)
                empleado.save()
                return redirect('profile', e_ficha=empleado.ficha)
        else:
            return render(request, 'addEmployee.html', {
                'form': form,
                'error': 'Ha ocurrido un error, intente de nuevo.'
            })

@staff_member_required(login_url='signin')
def editEmployee(request, e_ficha):
    empleado = get_object_or_404(Empleado, ficha=e_ficha)
    form = EmpleadoForm(instance=empleado)

    if request.method == 'GET':
        return render(request, 'addEmployee.html', {
            'form': form,
            'modificar': True,
            'empleado': empleado
        })
    else:
        form = EmpleadoForm(request.POST, request.FILES,
                            instance=empleado)  # Incluye request.FILES
        if form.is_valid():
            with transaction.atomic():
                empleado = form.save(commit=False)
                empleado.save()
                return redirect('profile', e_ficha=empleado.ficha)
        else:
            return render(request, 'addEmployee.html', {
                'form': form,
                'error': 'Ha ocurrido un error, intente de nuevo.'
            })

@staff_member_required(login_url='signin')
def deleteEmployee(request, e_ficha):
    empleado = get_object_or_404(Empleado, ficha=e_ficha)
    if request.method == 'GET':
        return render(request, 'egreso.html', {
            'empleado': empleado
        })
    else:
        try:
            with transaction.atomic():
                empleado.fechaEgreso = request.POST['fechaEgreso']
                empleado.save()
                return redirect('profile', e_ficha=empleado.ficha)
        except Exception as e:
            return render(request, 'egreso.html', {
                'empleado': empleado,
                'error': 'Ha ocurrido un error, intente de nuevo.'
            })

@staff_member_required(login_url='signin')
def reingreso(request, e_ficha):
    empleado = get_object_or_404(Empleado, ficha=e_ficha)
    if request.method == 'GET':
        return render(request, 'reingreso.html', {
            'empleado': empleado
        })
    else:
        try:
            with transaction.atomic():
                empleado.fechaEgreso = None
                empleado.save()
                return redirect('profile', e_ficha=empleado.ficha)
        except Exception as e:
            return render(request, 'reingreso.html', {
                'empleado': empleado,
                'error': 'Ha ocurrido un error, intente de nuevo.'
            })

@login_required
def addComentario(request, de_ficha, para_ficha):
    de = get_object_or_404(Empleado, ficha=de_ficha)
    para = get_object_or_404(Empleado, ficha=para_ficha)
    try:
        with transaction.atomic():
            comentario = comentarios(
                de=de, para=para, comentario=request.POST['comentario'])
            comentario.save()
            return redirect('profile', e_ficha=para.ficha)
    except Exception as e:
        return redirect('profile', e_ficha=para.ficha)
    
# view to see the current period
@staff_member_required(login_url='signin')
def periodos(request):
    periodos = Periodo.objects.all()
    return render(request, 'periodo.html', {
        'periodos': periodos
    })

@staff_member_required(login_url='signin')
def editPeriodo(request, id):
    periodo = get_object_or_404(Periodo, pk=id)

    if request.method == 'GET':
        form = PeriodoForm(initial={
            'fechaInicioEvaluaciones': periodo.fechaInicioEvaluaciones.strftime('%Y-%m-%d'),
            'fechaFinEvaluaciones': periodo.fechaFinEvaluaciones.strftime('%Y-%m-%d'),
        }, instance=periodo)
        return render(request, 'editPeriodo.html', {
            'form': form,
            'periodo': periodo,
            'error': 'Ha ocurrido un error, intente de nuevo.'
        })
    else:
        form = PeriodoForm(request.POST, instance=periodo)
        if form.is_valid():
            with transaction.atomic():
                periodo = form.save(commit=False)
                periodo.save()
                return redirect('periodos')
        else:
            return render(request, 'editPeriodo.html', {
                'form': form,
                'periodo': periodo,
                'error': 'Ha ocurrido un error, intente de nuevo.'
            })

@login_required
def objectives(request, e_ficha):
    empleado = get_object_or_404(Empleado, ficha=e_ficha)
    periodo = Periodo.objects.get(is_active=True)
    objetivos = empleado.objetivos_set.filter(periodo=periodo)   
    return render(request, 'objectives.html', {
        'empleado': empleado,
        'periodo': periodo,
        'objetivos': objetivos
    })

@login_required
def createObjectives(request, e_ficha):
    empleado = get_object_or_404(Empleado, ficha=e_ficha)
    periodo = Periodo.objects.get(is_active=True)
    if not empleado.distribucionObjetivos():
        messages.error(request, 'ERROR. No se ha definido la distribución de objetivos para el empleado. Por favor, contacte al administrador del sistema.')        
        
        return redirect('objectives', e_ficha=empleado.ficha)
    if request.method == 'GET':
        return render(request, 'crudObjectives.html', {
            'periodo': periodo,
            'empleado': empleado,
            'form': ObjectivesForm(empleado=empleado)            
        })
    else:
        form = ObjectivesForm(request.POST or None, empleado=empleado)
        if form.is_valid():
            with transaction.atomic():
                objetivo = form.save(commit=False)                
                objetivo.empleado = empleado
                objetivo.periodo = periodo
                objetivo.createdBy = request.user
                objetivo.save()
                messages.success(request, 'Objetivo creado exitosamente.')
                return redirect('objectives', e_ficha=empleado.ficha)
        else:
            return render(request, 'crudObjectives.html', {
                'form': form,
                'error': 'Ha ocurrido un error, intente de nuevo.',
                'periodo': periodo,
                'empleado': empleado,            
            })
    
    
    # if request.method == 'GET':
    #     return render(request, 'crudObjectives.html', {
    #         'periodo': periodo,
    #         'empleado': empleado,
    #         'tipos': empleado.distribucionObjetivos()})
    # else:
    #     form = ObjectivesForm(request.POST)
    #     if form.is_valid():
    #         newObjective = form.save(commit=False)
    #         newObjective.empleado = empleado
    #         newObjective.periodo = periodo
    #         newObjective.save()
    #         return redirect('objectives', e_ficha=empleado.ficha)
    #     else:
    #         return render(request, 'crudObjectives.html', {
    #             'form': form,
    #             'periodo': periodo,
    #             'empleado': empleado,
    #             'tipos': empleado.distribucionObjetivos(),
    #             'error': 'Ha ocurrido un error, intente de nuevo.'
    #         })
            
        

@login_required
def editObjectives(request, e_ficha, o_id):
    empleado = get_object_or_404(Empleado, ficha=e_ficha)
    objetivo = get_object_or_404(Objetivos, pk=o_id, empleado=empleado)
    
    if request.user != objetivo.createdBy and not request.user.is_staff and not empleado in request.user.empleado.subordinados():
        messages.error(request, 'ERROR. No tiene permisos para editar el objetivo.')
        return redirect('objectives', e_ficha=empleado.ficha)
    if objetivo.is_aproved:
        messages.error(request, 'ERROR. No se puede editar el objetivo porque ya fue aprobado.')
        return redirect('objectives', e_ficha=empleado.ficha)
    if request.method == 'GET':
        return render(request, 'editObjetive.html', {
            'objetivo': objetivo,
            'empleado': empleado,
            'form': ObjectivesForm(instance=objetivo)
        })
    else:
        form = ObjectivesForm(request.POST, instance=objetivo)
        newObjective = form.save(commit=False)
        newObjective.save()
        return redirect('objectives', e_ficha=empleado.ficha)

@login_required
def deleteObjectives(request, e_ficha, o_id):
    empleado = get_object_or_404(Empleado, ficha=e_ficha)
    objetivo = get_object_or_404(Objetivos, pk=o_id, empleado=empleado)
    if objetivo.is_aproved:
        messages.error(request, 'ERROR. No se puede eliminar el objetivo porque ya fue aprobado.')
        return redirect('objectives', e_ficha=empleado.ficha)
    if request.user != objetivo.createdBy:
        messages.error(request, 'ERROR. No se puede eliminar el objetivo porque no fue creado por usted.')
        return redirect('objectives', e_ficha=empleado.ficha)
    if objetivo.porcentaje() > 0:
        messages.error(request, 'ERROR. No se puede eliminar el objetivo se ha asignado un porcentaje de cumplimiento.')
        return redirect('objectives', e_ficha=empleado.ficha)
    if request.method == 'POST':
        objetivo.delete()
    return redirect('objectives', e_ficha=empleado.ficha)

@login_required(login_url='signin')
def approve_objective(request, e_ficha, o_id):
    empleado = get_object_or_404(Empleado, ficha=e_ficha)
    objetivo = get_object_or_404(Objetivos, pk=o_id, empleado=empleado)
    empleado_aprobador = request.user.empleado
    if objetivo.is_aproved:
        messages.error(request, 'ERROR. El objetivo ya fue aprobado.')
        return redirect('objectives', e_ficha=empleado.ficha)
    if not empleado in empleado_aprobador.subordinados() and not request.user.is_staff:
        messages.error(request, 'ERROR. No tiene permisos para aprobar el objetivo.')              
    elif request.method == 'POST':
        objetivo.is_aproved = True
        objetivo.aproved_by = request.user
        objetivo.save()
    else:
        messages.error(request, 'ERROR. No se pudo aprobar el objetivo.')
    return redirect('objectives', e_ficha=empleado.ficha)


@login_required
def activities(request, e_ficha, o_id):
    empleado = get_object_or_404(Empleado, ficha=e_ficha)
    objetivo = empleado.objetivos_set.get(pk=o_id)
    return render(request, 'activities.html', {
        'empleado': empleado,
        'objetivo': objetivo,
        'form': ObjectivesNotesForm(),
    })
    
@login_required
def add_note_to_objective(request, e_ficha, o_id):
    if request.method == 'POST':
        empleado = get_object_or_404(Empleado, ficha=e_ficha)
        objetivo = get_object_or_404(Objetivos, pk=o_id, empleado=empleado)
        form = ObjectivesNotesForm(request.POST)
        if form.is_valid():
            newNote = form.save(commit=False)
            newNote.objetivo = objetivo
            newNote.created_by = request.user
            newNote.save()
            return redirect('activities', e_ficha=empleado.ficha, o_id=objetivo.id)
        else:
            return redirect('activities', e_ficha=empleado.ficha, o_id=objetivo.id)
    else:
        messages.error(request, 'ERROR')
        return redirect('objectives', e_ficha=empleado.ficha)
    
@login_required   
def discard_note_from_objective(request, e_ficha, o_id, note_id):    
    empleado = get_object_or_404(Empleado, ficha=e_ficha)
    objetivo = get_object_or_404(Objetivos, pk=o_id, empleado=empleado)
    note = get_object_or_404(Objectives_notes, pk=note_id, objetivo=objetivo)
    if note.created_by != request.user:
        messages.error(request, 'ERROR. No se puede eliminar la nota porque no fue creada por usted.')
        return redirect('activities', e_ficha=empleado.ficha, o_id=objetivo.id)
    if request.method == 'POST':
        note.delete()
    return redirect('activities', e_ficha=empleado.ficha, o_id=objetivo.id)


@login_required
def updateActivities(request, e_ficha, o_id, a_id):
    empleado = get_object_or_404(Empleado, ficha=e_ficha)
    objetivo = empleado.objetivos_set.get(pk=o_id)
    actividad = get_object_or_404(Actividades, pk=a_id, objetivo=objetivo)
    if request.method == 'POST':
        actividad.estado = not actividad.estado
        actividad.save()
        return redirect('activities', e_ficha=empleado.ficha, o_id=objetivo.id)
    else:
        return redirect('activities', e_ficha=empleado.ficha, o_id=objetivo.id)

@login_required
def editActivities(request, e_ficha, o_id, a_id):
    empleado = get_object_or_404(Empleado, ficha=e_ficha)
    objetivo = empleado.objetivos_set.get(pk=o_id)
    actividad = get_object_or_404(Actividades, pk=a_id, objetivo=objetivo)
    if request.method == 'GET':
        return render(request, 'crudActivities.html', {
            'objetivo': objetivo,
            'empleado': empleado,
            'actividad': actividad,
            'form': ActivitiesForm(instance=actividad),
            'modificar': True
            
        })
    else:
        form = ActivitiesForm(request.POST, instance=actividad)
        newActivity = form.save(commit=False)
        newActivity.save()
        return redirect('activities', e_ficha=empleado.ficha, o_id=objetivo.id)

@login_required
def deleteActivities(request, e_ficha, o_id, a_id):
    empleado = get_object_or_404(Empleado, ficha=e_ficha)
    objetivo = empleado.objetivos_set.get(pk=o_id)
    actividad = get_object_or_404(Actividades, pk=a_id, objetivo=objetivo)
    if request.method == 'POST':
        actividad.delete()
    return redirect('activities', e_ficha=empleado.ficha, o_id=objetivo.id)

@login_required
def createActivities(request, e_ficha, o_id):
    empleado = get_object_or_404(Empleado, ficha=e_ficha)
    objetivo = empleado.objetivos_set.get(pk=o_id)
    if request.method == 'GET':
        return render(request, 'crudActivities.html', {
            'objetivo': objetivo,
            'empleado': empleado,
            'form': ActivitiesForm
        })
    else:
        form = ActivitiesForm(request.POST)
        newActivity = form.save(commit=False)
        newActivity.objetivo = objetivo
        newActivity.createdBy = request.user
        newActivity.save()

        return redirect('activities', e_ficha=empleado.ficha, o_id=objetivo.id)

@login_required
def dashboard_view(request):
    evaluacion = get_object_or_404(Evaluacion, id=10)
    return render(request, 'dashboard.html', {
        'valor': "ROJO",
        'evaluacion': evaluacion
    })

@login_required
def testDetails(request, e_ficha, eval_id):
    empleado = Empleado.objects.get(ficha=e_ficha)
    evaluacion = EvaluacionDesempeno.objects.get(pk=eval_id, empleado=empleado)

    objetivos = evaluacion.evaluacionobjetivo_set.all()
    forms = []

    for objetivo in objetivos:
        actividades = objetivo.objetivoactividad_set.all()
        formsAct = [ActividadesObjetivosEvaluacionForm(
            instance=actividad) for actividad in actividades]
        forms.append([ObjetivosEvaluacionForm(instance=objetivo), formsAct])

    competencias = evaluacion.evaluacioncompetencia_set.all()
    forms3 = []
    for competencia in competencias:
        forms3.append(CompetenciasEvaluacionForm(instance=competencia))

    return render(request, 'seeTest.html', {
        'forms': forms,
        'empleado': empleado,
        'evaluacion': evaluacion,
        'competencias': forms3,
    })

@login_required
def evaluar_desempeno(request, e_ficha):
    periodo = Periodo.objects.last()
    empleado = Empleado.objects.get(ficha=e_ficha)
    objetivos = Objetivos.objects.filter(periodo=periodo, empleado=empleado)
    if request.method == 'GET':
        competencias = CompetenciasEvaluacionForm(nivel=empleado.nivel())
        competenciasTodas = Competencias.objects.filter(nivel=empleado.nivel())
        forms = []
        for objetivo in objetivos:
            actividades = objetivo.actividades_set.all()
            formsAct = [ActividadesObjetivosEvaluacionForm(
                initial={'actividad': actividad.texto}) for actividad in actividades]
            forms.append([ObjetivosEvaluacionForm(
                initial={'objetivo': objetivo.texto}), formsAct])

        return render(request, 'doTest.html', {
            'forms': forms,
            'empleado': empleado,
            'competencias': competencias,
            'cantidadCompetencias': range(1, empleado.cargo.nivel.cantidadCompetencias + 1),
            'competenciasTodas': competenciasTodas

        })

    else:
        with transaction.atomic():
            evaluacion = EvaluacionDesempeno(
                periodo=periodo, empleado=empleado, resultadoObjetivos=float(request.POST.get('totalObj')), resultadoCompetencias=float(request.POST.get('totalCom')),
                deteccionCompetencia1=request.POST.get('deteccionCompetencia1'), deteccionCompetencia2=request.POST.get('deteccionCompetencia2'), deteccionCompetencia3=request.POST.get('deteccionCompetencia3'),
                deteccionTecConductual1=request.POST.get('deteccionTecConductual1'), deteccionTecConductual2=request.POST.get('deteccionTecConductual2'), deteccionTecConductual3=request.POST.get('deteccionTecConductual3'),
                comentarios=request.POST.get('comentarios'), estado=request.POST.get('estado'))
            evaluacion.save()
            j = 0
            for i, obj in enumerate(objetivos):
                actividades = obj.actividades()
                detalle = EvaluacionObjetivo()
                detalle.objetivo = obj
                detalle.evaluacion = evaluacion
                detalle.peso = request.POST.getlist('peso')[i]
                detalle.valor = request.POST.getlist('valor')[i]
                detalle.resultado = request.POST.getlist('resultado')[i]
                detalle.comentarios = request.POST.getlist('comentarios')[i]
                detalle.save()
                for act in actividades:
                    detalleAct = ObjetivoActividad()
                    detalleAct.objetivo = detalle
                    detalleAct.actividad = act
                    detalleAct.pesoActividad = request.POST.getlist('pesoActividad')[
                        j]
                    detalleAct.save()
                    j += 1

            for i in range(empleado.cargo.nivel.cantidadCompetencias):
                competencia = EvaluacionCompetencia()
                competencia.Evaluacion = evaluacion
                competencia.competencia = Competencias.objects.get(pk=request.POST.getlist('competencia')[
                    i])
                competencia.pesoCompetencia = request.POST.getlist('pesoCompetencia')[
                    i]
                competencia.resultadoCompetencia = request.POST.getlist(
                    'resultadoCompetencia')[i]
                competencia.save()

        return redirect('profile', e_ficha=empleado.ficha)

@login_required
def editEvaluacion(request, e_ficha, eval_id):
    empleado = Empleado.objects.get(ficha=e_ficha)
    evaluacion = EvaluacionDesempeno.objects.get(pk=eval_id, empleado=empleado)
    objetivos = evaluacion.evaluacionobjetivo_set.all()
    competencias = evaluacion.evaluacioncompetencia_set.all()
    if request.method == 'GET':
        forms = []
        for objetivo in objetivos:
            actividades = objetivo.objetivoactividad_set.all()
            formsAct = [ActividadesObjetivosEvaluacionForm(
                instance=actividad) for actividad in actividades]
            forms.append([ObjetivosEvaluacionForm(
                instance=objetivo), formsAct])

        forms3 = []
        for competencia in competencias:
            forms3.append(CompetenciasEvaluacionForm(instance=competencia))

        return render(request, 'editEvaluacion.html', {
            'forms': forms,
            'empleado': empleado,
            'evaluacion': evaluacion,
            'competencias': forms3
        })
    else:
        with transaction.atomic():
            evaluacion.resultadoObjetivos = float(
                request.POST.get('totalObj').replace(',', '.'))
            evaluacion.resultadoCompetencias = float(
                request.POST.get('totalCom').replace(',', '.'))
            evaluacion.deteccionCompetencia1 = request.POST.get(
                'deteccionCompetencia1')
            evaluacion.deteccionCompetencia2 = request.POST.get(
                'deteccionCompetencia2')
            evaluacion.deteccionCompetencia3 = request.POST.get(
                'deteccionCompetencia3')
            evaluacion.deteccionTecConductual1 = request.POST.get(
                'deteccionTecConductual1')
            evaluacion.deteccionTecConductual2 = request.POST.get(
                'deteccionTecConductual2')
            evaluacion.deteccionTecConductual3 = request.POST.get(
                'deteccionTecConductual3')
            evaluacion.comentarios = request.POST.get('comentarios')
            evaluacion.estado = request.POST.get('estado')
            evaluacion.save()
            for i, obj in enumerate(objetivos):
                actividades = obj.objetivoactividad_set.all()
                detalle = EvaluacionObjetivo.objects.get(
                    objetivo=obj.objetivo, evaluacion=evaluacion)
                detalle.peso = request.POST.getlist('peso')[i]
                detalle.valor = request.POST.getlist('valor')[i]
                detalle.resultado = request.POST.getlist('resultado')[i]
                detalle.comentarios = request.POST.getlist('comentarios')[i]
                detalle.save()
                for j, act in enumerate(actividades):
                    detalleAct = ObjetivoActividad.objects.get(
                        objetivo=detalle, actividad=act.actividad)
                    detalleAct.pesoActividad = request.POST.getlist('pesoActividad')[
                        j]
                    detalleAct.save()
            for i, comp in enumerate(competencias):
                comp.pesoCompetencia = request.POST.getlist('pesoCompetencia')[
                    i]
                comp.resultadoCompetencia = request.POST.getlist(
                    'resultadoCompetencia')[i]
                comp.save()
        return redirect('profile', e_ficha=empleado.ficha)

@login_required
def discardEvaluacion(request, e_ficha, eval_id):
    empleado = get_object_or_404(Empleado, ficha=e_ficha)
    evaluacion = get_object_or_404(
        EvaluacionDesempeno, pk=eval_id, empleado=empleado)

    if request.method == 'POST':
        evaluacion.delete()
        return redirect('profile', e_ficha=empleado.ficha)
    else:
        return redirect('profile', e_ficha=empleado.ficha)
    
@login_required
def evaluar_pns(request, e_ficha):
    empleado = get_object_or_404(Empleado, ficha=e_ficha)
    periodo = Periodo.objects.last()
    factores = Factores_de_evaluacion_PNS.objects.all()
    if request.method == 'POST':
        pass
    return render(request, 'evaluar_pns.html', {
        'empleado': empleado,
        'periodo': periodo,
        'factores': factores
    })

@ensure_csrf_cookie
def loginUser(request):
    # Si el usuario ya inició sesión, redireccionar a su perfil
    if request.user.is_authenticated:
        return redirect('profile', e_ficha=request.user.empleado.ficha)
    else:
        if request.method == 'GET':
            return render(request, 'login.html', {
                'form': AuthenticationForm
            })
        else:
            user = authenticate(
                request, username=request.POST['username'], password=request.POST['password'])
            if user is None:
                return render(request, 'login.html', {
                    'form': AuthenticationForm,
                    'error': 'Usuario o Contraseña equivocado'
                })
            else:
                login(request, user)
                empleado = get_object_or_404(Empleado, usuario=user)
                return redirect('profile', e_ficha=empleado.ficha)

@login_required
def logoutUser(request):
    if request.method == 'POST':
        messages.success(request, 'Sesión cerrada exitosamente.')
        logout(request)
    else:
        messages.error(request, 'ERROR. No se pudo cerrar la sesión.')
        
    return redirect('signin')
    


@login_required
def changePassword(request):
    if request.method == 'GET':
        return render(request, 'changePassword.html', {
            'form': PasswordChangeForm(request.user)
        })
    else:
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profile', e_ficha=request.user.empleado.ficha)
        else:
            return render(request, 'changePassword.html', {
                'form': form,
                'error': 'Ha ocurrido un error, intente de nuevo.'
            })

@staff_member_required(login_url='signin')
def seeCompetences(request):
    # cargar registros de nivel
    nivel = Nivel.objects.all()
    competencias = Competencias.objects.all()
    return render(request, 'seeCompetencias.html', {
        'niveles': nivel,
        'competencias': competencias,
    })
    
@staff_member_required(login_url='signin')
def competenceDetails(request, competence_id):
    competence = get_object_or_404(Competencias, pk=competence_id)
    return render(request, 'competencia.html', {'competencia': competence})

@staff_member_required(login_url='signin')
def addCompetence(request):
    if request.method == 'GET':
        return render(request, 'newCompetence.html', {
            'form': CompetenciasForm()
        })
    else:
        form = CompetenciasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('seeCompetences')
        else:
            return render(request, 'newCompetence.html', {
                'form': form,
                'error': 'Ha ocurrido un error, intente de nuevo.'
            })

@staff_member_required(login_url='signin')
def editCompetence(request, competence_id):
    competence = get_object_or_404(Competencias, pk=competence_id)
    if request.method == 'GET':
        return render(request, 'editCompetence.html', {
            'form': CompetenciasForm(instance=competence)
        })
    else:
        form = CompetenciasForm(request.POST, instance=competence)
        if form.is_valid():
            form.save()
            return redirect('seeCompetences')
        else:
            return render(request, 'editCompetence.html', {
                'form': form,
                'error': 'Ha ocurrido un error, intente de nuevo.'
            })

@staff_member_required(login_url='signin')
def seeCargos(request):
    niveles = Niveles.objects.all().order_by('valor')
    return render(request, 'seeCargos.html', {
        'niveles': niveles,
    })
    
@login_required(login_url='signin')
def cargoDetails(request, cargo_id):
    cargo = get_object_or_404(Cargo, pk=cargo_id)
    return render(request, 'cargo.html', {'cargo': cargo})

@staff_member_required(login_url='signin')
def editCargo(request, cargo_id):
    cargo = get_object_or_404(Cargo, pk=cargo_id)
    if request.method == 'GET':
        return render(request, 'cargo_crud.html', {
            'form': CargoForm(instance=cargo),
            'cargo': cargo
        })
    else:
        form = CargoForm(request.POST, instance=cargo)
        if form.is_valid():
            form.save()
            return redirect('seeCargos')
        else:
            messages.error(request, 'Ha ocurrido un error, intente de nuevo.')
            return render(request, 'cargo_crud.html', {
                'form': form(),
                'cargo': cargo
            })
            
@staff_member_required(login_url='signin')
def deactivate_cargo(request, cargo_id):
    cargo = get_object_or_404(Cargo, pk=cargo_id)
    if request.method == 'POST':
        cargo.is_active = False
        cargo.save()
    return redirect('seeCargos')


@staff_member_required(login_url='signin')
def addCargo(request):
    if request.method == 'GET':
        return render(request, 'cargo_crud.html', {
            'form': CargoForm()
        })
    else:
        form = CargoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('seeCargos')
        else:
            messages.error(request, 'Ha ocurrido un error, intente de nuevo.')
            return render(request, 'cargo_crud.html', {
                'form': form,
            })

@staff_member_required(login_url='signin')
def seeGerencias(request):
    direcciones = Direccion.objects.all()
    return render(request, 'seeGerencias.html', {
        'direcciones': direcciones,
    })

@staff_member_required(login_url='signin')
def editGerencia(request, gerencia_id):
    gerencia = get_object_or_404(Gerencia, pk=gerencia_id)
    if request.method == 'GET':
        return render(request, 'editGerencia.html', {
            'form': GerenciaForm(instance=gerencia)
        })
    else:
        form = GerenciaForm(request.POST, instance=gerencia)
        if form.is_valid():
            form.save()
            return redirect('seeGerencias')
        else:
            return render(request, 'editGerencia.html', {
                'form': form,
                'error': 'Ha ocurrido un error, intente de nuevo.'
            })

@staff_member_required(login_url='signin')
def addGerencia(request):
    if request.method == 'GET':
        return render(request, 'addGerencia.html', {
            'form': GerenciaForm()
        })
    else:
        form = GerenciaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('seeGerencias')
        else:
            return render(request, 'addGerencia.html', {
                'form': form,
                'error': 'Ha ocurrido un error, intente de nuevo.'
            })

@staff_member_required(login_url='signin')
def gerenciaDetails(request, gerencia_id):
    gerencia = get_object_or_404(Gerencia, pk=gerencia_id)
    return render(request, 'gerencia.html', {'gerencia': gerencia})

# view to see all direcciones
@staff_member_required(login_url='signin')
def seeDirecciones(request):
    direcciones = Direccion.objects.all()
    return render(request, 'seeDirecciones.html', {
        'direcciones': direcciones,
    })

@staff_member_required(login_url='signin')
def editDireccion(request, direccion_id):
    direccion = get_object_or_404(Direccion, pk=direccion_id)
    if request.method == 'GET':
        return render(request, 'editDireccion.html', {
            'form': DireccionForm(instance=direccion)
        })
    else:
        form = DireccionForm(request.POST, instance=direccion)
        if form.is_valid():
            form.save()
            return redirect('seeDirecciones')
        else:
            return render(request, 'editDireccion.html', {
                'form': form,
                'error': 'Ha ocurrido un error, intente de nuevo.'
            })

@staff_member_required(login_url='signin')
def addDireccion(request):
    if request.method == 'GET':
        return render(request, 'addDireccion.html', {
            'form': DireccionForm()
        })
    else:
        form = DireccionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('seeDirecciones')
        else:
            return render(request, 'addDireccion.html', {
                'form': form,
                'error': 'Ha ocurrido un error, intente de nuevo.'
            })

@login_required(login_url='signin')
def download_pdf(request, eval_id):
    logoPath = os.path.join(settings.BASE_DIR, 'static', 'GCLOGO.png')
    print(logoPath)
    evaluacion = get_object_or_404(EvaluacionDesempeno, id=eval_id)
    objetivos = EvaluacionObjetivo.objects.filter(evaluacion=evaluacion)
    competencias = EvaluacionCompetencia.objects.filter(Evaluacion=evaluacion)
    template_path = 'evaluacion_pdf.html'
    context = {'evaluacion': evaluacion, 'Objetivos': objetivos,
               'Competencias': competencias, 'logoPath': logoPath}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # If you want to download the PDF instead of showing it in the browser, use the following line instead:
    response['Content-Disposition'] = 'attachment; filename="evaluacion.pdf"'
    # response['Content-Disposition'] = 'filename="evaluacion.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF')
    return response

@login_required(login_url='signin')
def system_parameters(request):
    return render(request, 'system_parameters.html')

@login_required(login_url='signin')
def system_parameters_niveles(request):
    niveles = Niveles.objects.all().order_by('valor')
    return render(request, 'system_parameters_niveles.html', {
        'niveles': niveles
    })
    
@login_required(login_url='signin')
def system_parameters_niveles_detail(request,nivel):
    nivel = get_object_or_404(Niveles, valor=nivel)
    return render(request, 'system_parameters_niveles_detail.html', {
        'nivel': nivel
    })
  
@login_required(login_url='signin')
def system_parameter_percentaje_distribution(request):
    departamentos = Departamento.objects.all()
    return render(request, 'system_parameter_percentaje_distribution.html', {
        'departamentos': departamentos
    })

@login_required(login_url='signin')
def system_parameter_percentaje_distribution_department(request, department):
    departamento = get_object_or_404(Departamento, nombre=department)
    niveles = Niveles.objects.all().order_by('valor')
    return render(request, 'system_parameter_percentaje_distribution_department.html', {
        'niveles': niveles,
        'departamento': departamento
    })

@login_required(login_url='signin')
def system_parameter_percentaje_distribution_department_nivel(request, department, nivel):
    departamento = get_object_or_404(Departamento, nombre=department)
    nivel = get_object_or_404(Niveles, valor=nivel)
    distribucion = Distribucion.objects.get(departamento=departamento, nivel=nivel)
    distribucionObjetivos = distribucion.distribucionobjetivo_set.all()
    suma = 0
    for dist in distribucionObjetivos:
        suma += dist.peso 

    return render(request, 'system_parameter_percentaje_distribution_department_nivel.html', {
        'nivel': nivel,
        'departamento': departamento,
        'distribucion': distribucion,
        'distribucionObjetivos': distribucionObjetivos,
        'suma': suma,
    })

@login_required(login_url='signin')
def system_parameter_percentaje_distribution_department_nivel_distribution(request, department, nivel, distribucion):
    departamento = get_object_or_404(Departamento, nombre=department)
    nivel = get_object_or_404(Niveles, valor=nivel)
    distribucion = get_object_or_404(Distribucion, pk=distribucion)
    if request.method == 'GET':
        return render(request, 'system_parameter_percentaje_distribution_department_nivel_distribution.html', {
            'nivel': nivel,
            'departamento': departamento,
            'distribucion': distribucion,
            'form': DistribucionObjetivoForm()
        })
    else:
        form = DistribucionObjetivoForm(request.POST)
        if form.is_valid():
            peso = form.cleaned_data['peso']
            tipo = form.cleaned_data['tipo']
            distribucion_objetivo = DistribucionObjetivo.objects.filter(distribucion=distribucion, tipo=tipo).first()
            if peso == 0:
                form.add_error('peso', 'Peso cannot be 0')
            elif distribucion_objetivo:
                form.add_error('nombre', 'Distribucion objetivo with the same name already exists')
            else:
                newDistribucionObjetivo = form.save(commit=False)
                newDistribucionObjetivo.distribucion = distribucion
                newDistribucionObjetivo.save()
                return redirect('systemparameterpercentajedistributiondepartmentnivel', department=department, nivel=nivel.valor)
    return render(request, 'system_parameter_percentaje_distribution_department_nivel_distribution.html', {
        'nivel': nivel,
        'departamento': departamento,
        'distribucion': distribucion,
        'form': form
    })

@login_required(login_url='signin')
def system_parameter_percentaje_distribution_department_nivel_distribution_edit(request, department, nivel, distribucion, dist_obj):
    departamento = get_object_or_404(Departamento, nombre=department)
    nivel = get_object_or_404(Niveles, valor=nivel)
    distribucion = get_object_or_404(Distribucion, pk=distribucion)
    dist_obj = get_object_or_404(DistribucionObjetivo, pk=dist_obj)
    if request.method == 'GET':
        return render(request, 'system_parameter_percentaje_distribution_department_nivel_distribution.html', {
            'nivel': nivel,
            'departamento': departamento,
            'distribucion': distribucion,
            'dist_obj': dist_obj,
            'form': DistribucionObjetivoForm(instance=dist_obj)
        })
    else:
        form = DistribucionObjetivoForm(request.POST, instance=dist_obj)
        if form.is_valid():
            form.save()
            return redirect('systemparameterpercentajedistributiondepartmentnivel', department=department, nivel=nivel.valor)
    return render(request, 'system_parameter_percentaje_distribution_department_nivel_distribution.html', {
        'nivel': nivel,
        'departamento': departamento,
        'distribucion': distribucion,
        'dist_obj': dist_obj,
        'form': form
    })
    

@login_required(login_url='signin')
def export_cargos(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="cargos.xlsx"'

    cargos = Cargo.objects.all().order_by('nivel__valor')
    cargos_data = []
    for cargo in cargos:
        cargos_data.append({
            'Nivel': cargo.nivel.valor,
            'Nombre': cargo.nombreText,
            'Superior': cargo.supervisor.nombreText if cargo.supervisor else '',
            'Gerencia': cargo.gerencia.nombreText if cargo.gerencia else '',
            'Direccion': cargo.direccion.nombre if cargo.direccion else '',      
            'Relativo en Infocent' : cargo.nombre_infocent if cargo.nombre_infocent else '',
                        

        })

    df = pd.DataFrame(cargos_data)
    df.to_excel(response, index=False)

    return response

@login_required(login_url='signin')
def export_gerencias(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="gerencias.xlsx"'

    gerencias = Gerencia.objects.all()
    gerencias_data = []
    for gerencia in gerencias:
        gerencias_data.append({
            'Nombre': gerencia.nombreText,
            'Direccion': gerencia.direccion.nombre if gerencia.direccion else '',                        
        })

    df = pd.DataFrame(gerencias_data)
    df.to_excel(response, index=False)

    return response

@login_required(login_url='signin')
def export_empleados(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="empleados.xlsx"'

    empleados = Empleado.objects.exclude(fechaEgreso__isnull=False)
    empleados_data = []
    for empleado in empleados:        
        empleados_data.append({
            'Nivel': empleado.cargo.nivel.valor if empleado.cargo else '',
            'CECO': empleado.ceco,
            'Ficha': empleado.ficha,
            'Cedula': empleado.cedula,
            'Nombre': empleado.nombre,
            'Apellido': empleado.apellido,
            'Cargo': empleado.cargo.nombreText if empleado.cargo else '',
            'Supervisor': empleado.supervisor(),
            'Gerencia': empleado.cargo.gerencia.nombreText if empleado.cargo.gerencia else '',
            'Direccion': empleado.cargo.gerencia.direccion.nombre if empleado.cargo.gerencia else '',                     
            'Departamento': empleado.cargo.gerencia.departamento.nombre if empleado.cargo.gerencia else '',                                 
        })

    df = pd.DataFrame(empleados_data)
    df.to_excel(response, index=False)

    return response

@login_required(login_url='signin')
def import_cargos(request):
    if request.method == 'GET':
        return render(request, 'import_cargos.html')
    else:
        cargos_file = request.FILES['cargos_file']
        cargos = pd.read_excel(cargos_file)
        for index, row in cargos.iterrows():
            print(f'Nivel: {row["Nivel"]}')
            nivel = Niveles.objects.get(valor=row['Nivel'])
            nombre = row['Nombre']
            
            superior = Cargo.objects.filter(nombreText=row['Superior']).first()
            gerencia = Gerencia.objects.filter(nombreText=row['Gerencia']).first()
            direccion = Direccion.objects.filter(nombre=row['Direccion']).first()

            # Check if a cargo with the same name already exists
            existing_cargo = Cargo.objects.filter(nombreText=nombre).first()
            if existing_cargo:
                # Update the existing cargo
                existing_cargo.nivel = nivel
                existing_cargo.supervisor = superior
                existing_cargo.gerencia = gerencia
                existing_cargo.direccion = direccion
                if row['Relativo en Infocent'] == 'nan':
                    existing_cargo.nombre_infocent = ''
                else:                    
                    existing_cargo.nombre_infocent = row['Relativo en Infocent']     
                    try:
                        existing_cargo.nombre_infocent = existing_cargo.nombre_infocent.strip() 
                    except:
                        pass
                
                existing_cargo.save()
            else:
                # Create a new cargo
                newCargo = Cargo(nivel=nivel, nombreText=nombre, supervisor=superior, gerencia=gerencia, direccion=direccion, nombre_infocent=row['Relativo en Infocent'])
                newCargo.save()
                
        return redirect('systemparameters')
    
@login_required(login_url='signin')
def import_empleados(request):
    if request.method == 'GET':
        return render(request, 'import_empleados.html')
    else:
        print('Importando empleados...')
        empleados_file = request.FILES['empleados_file']
        empleados = pd.read_excel(empleados_file)
        print('Empleados leídos...')
        for index, row in empleados.iterrows():
            nombre_infocent = row['CARGO']
            if nombre_infocent == 'nan':
                print(f'No se encontró el cargo {row["CARGO"]} en el sistema')
                continue
            cargo = Cargo.objects.filter(nombre_infocent=nombre_infocent.strip()).first()
            
            if cargo is None:
                print(f'No se encontró el cargo {row["CARGO"]} en el sistema')
                continue
            ceco = row['CECO']            
            ficha = row['FICHA']
            cedula = row['CEDULA']
            nombre = row['NOMBRES']
            apellido = row['APELLIDOS']
            fechaIngreso = row['FECHA DE INGRESO']          

            # Check if an employee with the same ficha already exists
            existing_empleado = Empleado.objects.filter(ficha=ficha).first()
            print(f'Procesando empleado {ficha}')
            if existing_empleado:
                try:
                    username = f"{nombre.split()[0].lower()}.{apellido.split()[0].lower()}"
                    password = '1234'
                    user = User.objects.create_user(username=username, password=password)
                    existing_empleado.usuario = user
                except:
                    print(f'Error creating user for {ficha}') 
                existing_empleado.cargo = cargo
                existing_empleado.ceco = ceco
                existing_empleado.cedula = cedula
                existing_empleado.nombre = nombre
                existing_empleado.apellido = apellido
                existing_empleado.fechaIngreso = fechaIngreso
                existing_empleado.save()
                print(f'Empleado {ficha} actualizado')
   
            else:
                try:
                    username = f"{nombre.split()[0].lower()}.{apellido.split()[0].lower()}"
                    password = '1234'
                    user = User.objects.create_user(username=username, password=password)

                except:
                    print(f'Error creating user for {ficha}') 
                newEmpleado = Empleado(cargo=cargo, ceco=ceco, ficha=ficha, cedula=cedula, nombre=nombre, apellido=apellido, fechaIngreso=fechaIngreso, usuario=user)
                newEmpleado.save()
            print(f'Empleado {ficha} importado')
        print('Empleados importados')
                
        return redirect('systemparameters')
    
@login_required(login_url='signin')
def competencias_by_my_level(request):
    empleado = request.user.empleado
    nivel = empleado.nivel()
    competencias = Competencias.objects.filter(nivel=nivel)
    return render(request, 'competencias_level.html', {
        'competencias': competencias,
        'nivel': nivel
    })

class Preguntas_Frecuentes_List(ListView):
    model = Preguntas_Frecuentes
    template_name = 'preguntas_frecuentes.html'
    context_object_name = 'preguntas_frecuentes'
    
@login_required(login_url='signin')
def announcements_view(request):
    announcements = Announcements.objects.all().order_by('-date')
    return render(request, 'announcements.html', {
        'announcements': announcements
    })
    
@staff_member_required(login_url='signin')
def announcements_add(request):
    if request.method == 'GET':
        return render(request, 'announcements_add.html', {
            'form': AnnouncementForm()
        })
    else:
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('announcements')
        else:
            return render(request, 'announcements_add.html', {
                'form': form,
                'error': 'Ha ocurrido un error, intente de nuevo.'
            })
    
@login_required(login_url='signin')
def company_objectives_view(request):
    periodo = Periodo.objects.get(is_active=True)
    company_objectives = Company_Objectives.objects.filter(period=periodo)
    return render(request, 'company_objectives.html', {
        'periodo': periodo,
        'company_objectives': company_objectives
    })
    
@staff_member_required(login_url='signin')
def company_objectives_add(request):
    period = Periodo.objects.get(is_active=True)
    if request.method == 'GET':
        return render(request, 'company_objectives_add.html', {
            'form': CompanyObjectivesForm(),
            'periodo': period            
        })
    else:
        form = CompanyObjectivesForm(request.POST)
        if form.is_valid():            
            newCompanyObjective = form.save(commit=False)
            newCompanyObjective.period = period
            newCompanyObjective.save()
            messages.success(request, 'Objetivo agregado')
            return redirect('companyobjectives')
        else:
            messages.error(request, 'Ha ocurrido un error, intente de nuevo.')
            return render(request, 'company_objectives_add.html', {
                'form': form,
                'periodo': period
            })
            
@staff_member_required(login_url='signin')
def company_objectives_edit(request, obj_id):
    company_objective = get_object_or_404(Company_Objectives, pk=obj_id)
    if request.method == 'GET':
        return render(request, 'company_objectives_add.html', {
            'form': CompanyObjectivesForm(instance=company_objective),
            'company_objective': company_objective
        })
    else:
        form = CompanyObjectivesForm(request.POST, instance=company_objective)
        if form.is_valid():
            form.save()
            messages.success(request, 'Objetivo actualizado')
            return redirect('companyobjectives')
        else:
            messages.error(request, 'Ha ocurrido un error, intente de nuevo.')
            return render(request, 'company_objectives_add.html', {
                'form': form,
                'company_objective': company_objective
            })

@staff_member_required(login_url='signin')
def company_objectives_delete(request, obj_id):
    company_objective = get_object_or_404(Company_Objectives, pk=obj_id)
    if request.method == 'POST':
        company_objective.delete()
        messages.success(request, 'Objetivo eliminado')
    return redirect('companyobjectives')

@staff_member_required(login_url='signin')
def generate_report_per_department(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=reporte_departamentos.xlsx'
    workbook = Workbook()
    # Remove the default sheet created
    workbook.remove(workbook.active)
    departamentos = Departamento.objects.all()

    for departamento in departamentos:
        worksheet = workbook.create_sheet(title=departamento.nombre)
        worksheet.append([departamento.nombre])
        worksheet.append(['Objetivos Generales', departamento.get_amount_objetivos_generales()])
        worksheet.append(['Objetivos Especificos', departamento.get_amount_objetivos_especificos()])
        worksheet.append(['Ficha', 'Nombre', 'Apellido', 'Cargo', 'Gerencia', 'Direccion', 'Objetivos Generales', 'Objetivos Especificos', 'Status'])
        empleados = Empleado.objects.filter(cargo__gerencia__departamento=departamento, fechaEgreso__isnull=True)
        for empleado in empleados:
            worksheet.append([empleado.ficha, empleado.nombre, empleado.apellido, empleado.cargo.nombreText, empleado.cargo.gerencia.nombreText, empleado.cargo.gerencia.direccion.nombre, empleado.cantidadObjetivos(), empleado.cantidadActividades(),'Si' if empleado.cantidadObjetivos() > 0 else 'No'])
        
        # Adjust column widths
        for column in worksheet.columns:
            max_length = 0
            column = [cell for cell in column]
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2)
            worksheet.column_dimensions[column[0].column_letter].width = adjusted_width

    workbook.save(response)
    return response
