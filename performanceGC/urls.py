from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
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
    path('systemparameters/import/cargos/', views.import_cargos, name='importcargos'),
    path('systemparameters/import/empleados/', views.import_empleados, name='importempleados'),    
    path('debugTests/', views.debugTests, name='debugtests'),
    path('signin/', views.loginUser, name='signin'),
    path('signout/', views.logoutUser, name='signout'),
    path('newUser/', views.createUser, name='newUser'),
    path('users/', views.users, name='users'),
    path('profile/<int:e_ficha>/', views.profileView, name='profile'),
    path('profile/<int:e_ficha>/objectives/', views.objectives, name='objectives'),
    path('profile/<int:e_ficha>/objectives/new/', views.createObjectives, name='newobjective'),
    path('profile/<int:e_ficha>/objectives/obj_<int:o_id>/edit/', views.editObjectives, name='editobjective'),
    path('profile/<int:e_ficha>/objectives/obj_<int:o_id>/discard/', views.deleteObjectives, name='discardobjective'),
    path('profile/<int:e_ficha>/objectives/obj_<int:o_id>/', views.activities, name='activities'),
    path('profile/<int:e_ficha>/objectives/obj_<int:o_id>/act_<int:a_id>/complete/', views.updateActivities, name='completeactivity'),
    path('profile/<int:e_ficha>/objectives/obj_<int:o_id>/act_<int:a_id>/discard/', views.deleteActivities, name='discardactivity'),
    path('profile/<int:e_ficha>/objectives/obj_<int:o_id>/act_<int:a_id>/edit/', views.editActivities, name='editactivities'),
    path('profile/<int:e_ficha>/objectives/obj_<int:o_id>/add/', views.createActivities, name='newactivity'),
    path('profile/<int:e_ficha>/test_<int:eval_id>/', views.testDetails, name='testdetails'),
    path('profile/<int:e_ficha>/newselftest/', views.evaluar_desempeno, name='newselftest'),
    path('profile/<int:e_ficha>/test_pns/', views.evaluar_pns, name='evaluarpns'),
    path('profile/<int:e_ficha>/edit_test_<int:eval_id>/', views.editEvaluacion, name='edittest'), 
    path('profile/<int:e_ficha>/test_<int:eval_id>/discard', views.discardEvaluacion, name='discardtest'),
    path('search/', views.masterEmployee, name='search'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('newEmployee/', views.addEmployee, name='newemployee'),
    path('editEmployee/<int:e_ficha>/', views.editEmployee, name='editemployee'),
    path('deleteEmployee/<int:e_ficha>/', views.deleteEmployee, name='deleteemployee'),
    path('restoreEmployee/<int:e_ficha>/', views.reingreso, name='restoreEmployee'),
    path('changePassword/', views.changePassword, name='changePassword'),
    path('periodos/', views.periodos, name='periodos'),
    path('periodos/<int:id>/', views.editPeriodo, name='editperiodo'),    
    path('seeCompetences/', views.seeCompetences, name='seeCompetences'),
    path('addCompetence/', views.addCompetence, name='addCompetence'),
    path('editCompetence/<int:competence_id>/', views.editCompetence, name='editCompetence'),
    path('seeCargos/', views.seeCargos, name='seeCargos'),
    path('editCargo/<int:cargo_id>/', views.editCargo, name='editCargo'),
    path('addCargo/', views.addCargo, name='addCargo'),
    path('seeGerencias/', views.seeGerencias, name='seeGerencias'),
    path('gerencia/<int:gerencia_id>', views.gerenciaDetails, name = 'gerenciadetails'),
    path('addGerencia/', views.addGerencia, name='addGerencia'),
    path('editGerencia/<int:gerencia_id>/', views.editGerencia, name='editGerencia'),
    path('seeDirecciones/', views.seeDirecciones, name='seeDirecciones'),
    path('addDireccion/', views.addDireccion, name='addDireccion'),
    path('editDireccion/<int:direccion_id>/', views.editDireccion, name='editDireccion'),
    path('printTest/<int:eval_id>/', views.download_pdf, name='printTest'),
    path('profile/<int:para_ficha>/newcommmnent_<int:de_ficha>', views.addComentario, name='newcommmnent'),
    path('faq/', views.Preguntas_Frecuentes_List.as_view(), name='faq'),
    path('competences/' , views.competencias_by_my_level, name='competences'),
    path('announcements/', views.announcements_view, name='announcements'),
    path('announcements/new/', views.announcements_add, name='announcements_add'),
    path('companyobjectives/', views.company_objectives_view, name='companyobjectives'),

]
