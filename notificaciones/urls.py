from django.urls import path
from . import views

app_name = 'notificaciones'

urlpatterns = [
    path('', views.ListaNotificacionesView.as_view(), name='lista'),
    path('marcar/<int:pk>/', views.marcar_como_leida, name='marcar_leida'),
    path('marcar-todas/', views.marcar_todas_leidas, name='marcar_todas'),
]