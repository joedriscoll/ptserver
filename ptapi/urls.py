from django.conf.urls import patterns, url

from ptapi import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'login', views.login, name = 'login'),
    url(r'logPain', views.logPain, name = 'logPain'),
    url(r'register', views.register, name = 'register'),
    url(r'settings', views.getSettings, name = 'settings'),
    url(r'getPatients', views.getPatients, name = 'getPatients'),
     url(r'assignPT', views.addPair, name = 'addPair')
)