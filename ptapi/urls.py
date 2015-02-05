from django.conf.urls import patterns, url

from ptapi import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'login', views.login, name = 'login'),
    url(r'logPain', views.logPain, name = 'logPain'),
    url(r'register', views.register, name = 'register'),
    url(r'settings', views.getSettings, name = 'settings'),
    url(r'getPatients', views.getPatients, name = 'getPatients'),
    url(r'getActivity', views.getActivity, name = 'getActivity'),
    url(r'updateExercise', views.updateExercise, name = 'updateExercise'), 
    url(r'getExercisesForPatient', views.getExercisesForPatient, name = 'getExercisesForPatient'),
    url(r'patientsExerciseData', views.getPatientsExerciseData, name = 'patientsExerciseData'),
    url(r'editExerciseData', views.editExerciseData, name = 'editExerciseData'), 
    url(r'addNewExercise', views.addNewExercise, name = 'addNewExercise'), 
    url(r'addNewInstance', views.postExerciseInstance, name = 'addNewInstance'),
    url(r'getAchievements', views.getAchievements, name = 'Achievements'),
     url(r'assignPT', views.addPair, name = 'addPair')
     
)