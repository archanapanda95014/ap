from django.conf.urls import url
from . import views          
urlpatterns = [
    url(r'^$', views.index),
    url(r'register$', views.register),
    url(r'login$', views.login),
    url(r'successLogin$', views.successLogin), 
    url(r'addQuote$', views.addQuote),
    url(r'quoteDisplay$', views.successLogin),
    url(r'logout$', views.logout),
    url(r'showUserQuotes/(?P<num>\d+)$', views.showUserQuotes),
    url(r'delete/(?P<num>\d+)$', views.delete),
    url(r'edit/(?P<num>\d+)$', views.edit),
    url(r'updateUser(?P<num>\d+)$', views.updateUser),
]