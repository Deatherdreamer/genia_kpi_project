from django.urls import path

from . import views



urlpatterns = [
    path('', views.index, name='index'),
 
    # path('debugTests/', views.debugTests, name='debugtests'),
    
    # USER AUTHENTICATION
    # path('signin/', views.loginUser, name='signin'),
    # path('signout/', views.logoutUser, name='signout'),
    path('newUser/', views.createUser, name='newUser'),
    path('users/', views.users, name='users'),
    
    # URLS PARA EMPLEADOS
    path('profile/<int:e_ficha>/', views.profileView, name='profile'),
    path('profile/<int:e_ficha>/objectives/', views.objectives, name='objectives'),
    path('profile/<int:e_ficha>/objectives/new/', views.createObjectives, name='newobjective'),
    path('profile/<int:e_ficha>/objectives/obj_<int:o_id>/edit/', views.editObjectives, name='editobjective'),
    path('profile/<int:e_ficha>/objectives/obj_<int:o_id>/discard/', views.deleteObjectives, name='discardobjective'),
    path('profile/<int:e_ficha>/objectives/obj_<int:o_id>/', views.activities, name='activities'),
    path('profile/<int:e_ficha>/objectives/obj_<int:o_id>/approve/', views.approve_objective , name='approveobjective'),
    path('profile/<int:e_ficha>/objectives/obj_<int:o_id>/disapprove/', views.disapprove_objective , name='disapproveobjective'),
    path('profile/<int:e_ficha>/objectives/obj_<int:o_id>/new_note/', views.add_note_to_objective, name='new_note'),
    path('profile/<int:e_ficha>/objectives/obj_<int:o_id>/discard_note/<int:note_id>/', views.discard_note_from_objective, name='discard_note'),
    path('profile/<int:e_ficha>/objectives/obj_<int:o_id>/act_<int:a_id>/complete/', views.updateActivities, name='completeactivity'),
    path('profile/<int:e_ficha>/objectives/obj_<int:o_id>/act_<int:a_id>/discard/', views.deleteActivities, name='discardactivity'),
    path('profile/<int:e_ficha>/objectives/obj_<int:o_id>/act_<int:a_id>/edit/', views.editActivities, name='editactivities'),
    path('profile/<int:e_ficha>/objectives/obj_<int:o_id>/add/', views.createActivities, name='newactivity'),
    path('profile/<int:e_ficha>/test_<int:eval_id>/', views.testDetails, name='testdetails'),
    path('profile/<int:e_ficha>/newselftest/', views.evaluar_desempeno, name='newselftest'),
    path('profile/<int:e_ficha>/test_pns/', views.evaluar_pns, name='evaluarpns'),
    path('profile/<int:e_ficha>/edit_test_<int:eval_id>/', views.editEvaluacion, name='edittest'), 
    path('profile/<int:e_ficha>/test_<int:eval_id>/discard/', views.discardEvaluacion, name='discardtest'),
    path('search/', views.masterEmployee, name='search'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('newEmployee/', views.addEmployee, name='newemployee'),
    path('editEmployee/<int:e_ficha>/', views.editEmployee, name='editemployee'),
    path('deleteEmployee/<int:e_ficha>/', views.deleteEmployee, name='deleteemployee'),
    path('restoreEmployee/<int:e_ficha>/', views.reingreso, name='restoreEmployee'),
    path('changePassword/', views.changePassword, name='changePassword'),
    
    # URLS PARA PERIODOS    
    path('periodos/', views.periodos, name='periodos'),
    path('periodos/<int:id>/', views.periodo_details, name='periodo_details'),
    path('periodos/<int:id>/edit/', views.editPeriodo, name='editperiodo'),
    
    # URLS COMPETENCIAS    
    path('competences/', views.seeCompetences, name='seeCompetences'),
    path('competences/my_level/' , views.competencias_by_my_level, name='competences'),    
    path('competences/new', views.addCompetence, name='addCompetence'),
    path('competences/<int:competence_id>/', views.competenceDetails, name='competencedetails'),
    path('competences/<int:competence_id>/modify', views.editCompetence, name='editCompetence'),

    # URLS DIRECCIONES
    path('direcciones/', views.seeDirecciones, name='seeDirecciones'),
    path('direcciones/new', views.addDireccion, name='addDireccion'),
    path('direcciones/direccion_<int:direccion_id>/', views.direccionDetails, name='direcciondetails'),
    path('direcciones/direccion_<int:direccion_id>/modify', views.editDireccion, name='editDireccion'),  
   
    # URLS GERENCIAS
    path('gerencias/', views.seeGerencias, name='seeGerencias'),
    path('gerencias/gerencia_<int:gerencia_id>/', views.gerenciaDetails, name = 'gerenciadetails'),
    path('gerencias/new/', views.addGerencia, name='addGerencia'),
    path('gerencias/gerencia_<int:gerencia_id>/modify/', views.editGerencia, name='editGerencia'),
    
    # URLS CARGOS
    path('cargos/', views.seeCargos, name='seeCargos'),    
    path('cargos/new/', views.addCargo, name='addCargo'),
    path('cargos/cargo_<int:cargo_id>/', views.cargoDetails, name = 'cargodetails'),
    path('cargos/cargo_<int:cargo_id>/modify', views.editCargo, name='editCargo'),
    path('cargos/cargo_<int:cargo_id>/deactivate/', views.deactivate_cargo, name='deactivatecargo'),  

    path('printTest/<int:eval_id>/', views.download_pdf, name='printTest'),
    path('profile/<int:para_ficha>/newcommmnent_<int:de_ficha>/', views.addComentario, name='newcommmnent'),
    path('faq/', views.Preguntas_Frecuentes_List.as_view(), name='faq'),
    
    # URLS PARA OBJETIVOS DE LA EMPRESA
    path('companyobjectives/', views.company_objectives_view, name='companyobjectives'),
    path('companyobjectives/new/', views.company_objectives_add, name='companyobjectives_add'),
    path('companyobjectives/edit/<int:obj_id>/', views.company_objectives_edit, name='companyobjectives_edit'),
    path('companyobjectives/delete/<int:obj_id>/', views.company_objectives_delete, name='companyobjectives_delete'),
    
    # URLS PARA ANUNCIOS    
    path('announcements/', views.announcements_view, name='announcements'),
    path('announcements/new/', views.announcements_add, name='announcements_add'), 
    path('announcements/<int:announcement_id>/edit/', views.announcements_edit, name='announcements_edit'),
    path('announcements/<int:announcement_id>/delete/', views.announcements_delete, name='announcements_delete'),
    
    
    # URLS PARAMETROS DEL SISTEMA
    path('systemparameters/', views.system_parameters, name='systemparameters'),
    path('systemparameters/niveles', views.system_parameters_niveles, name='systemparametersniveles'),
    path('systemparameters/niveles/nivel_<str:nivel>', views.system_parameters_niveles_detail, name='systemparametersnivelesdetail'),
    path('systemparameters/percentajedistribution/', views.system_parameter_percentaje_distribution, name='systemparameterpercentajedistribution'),
    path('systemparameters/percentajedistribution/<str:department>/', views.system_parameter_percentaje_distribution_department, name='systemparameterpercentajedistributiondepartment'),
    path('systemparameters/percentajedistribution/<str:department>/nivel_<str:nivel>/', views.system_parameter_percentaje_distribution_department_nivel, name='systemparameterpercentajedistributiondepartmentnivel'),
    path('systemparameters/percentajedistribution/<str:department>/nivel_<str:nivel>/<int:distribucion>/add/', views.system_parameter_percentaje_distribution_department_nivel_distribution, name='systemparameterpercentajedistributiondepartmentniveldistribution'),
    path('systemparameters/percentajedistribution/<str:department>/nivel_<str:nivel>/<int:distribucion>/<int:dist_obj>/edit/', views.system_parameter_percentaje_distribution_department_nivel_distribution_edit, name='systemparameterpercentajedistributiondepartmentniveldistributionedit'), 
    path('systemparameters/export/cargos/', views.export_cargos, name='exportcargos'),
    path('systemparameters/export/gerencias/', views.export_gerencias, name='exportgerencias'),
    path('systemparameters/export/empleados/', views.export_empleados, name='exportempleados'),
    path('systemparameters/export/reportsdepartment/', views.generate_report_per_department, name='exportreportsdepartment'),
    path('systemparameters/import/cargos/', views.import_cargos, name='importcargos'),
    path('systemparameters/import/empleados/', views.import_empleados, name='importempleados'),   
    path('systemparameters/import/upload_and_update_user_info/', views.upload_and_update_user_info, name='upload_and_update_user_info'),   
]
