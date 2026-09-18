from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    path('', views.reportes_dashboard, name='dashboard'),
    path('clientes/', views.reporte_clientes, name='clientes'),
    path('clientes/excel/', views.exportar_clientes_excel, name='clientes_excel'),
    path('transferencias/', views.reporte_transferencias, name='transferencias'),
]