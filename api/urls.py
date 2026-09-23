from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.getdata, name='datos'),
    path('clientes/', views.get_clientes, name='clientes'),
]