from django.conf.urls import patterns, url

from ptapi import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'login', views.login, name = 'login'),
    url(r'logpain', views.logPain, name = 'logpain'),
    url(r'register', views.register, name = 'register'),
    url(r'settings', views.getSettings, name = 'settings')
)