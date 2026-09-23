from django.urls import path, include
from . import views

app_name = 'api'

urlpatterns = [
    path('', views.getdata, name='datos'),
    path('clientes/', views.clientes, name='clientes'),
    path('clientes/<int:id>', views.get_cliente, name='get_cliente'),
]