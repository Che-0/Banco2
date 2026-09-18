from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('usuarios/', views.ListaUsuariosView.as_view(), name='lista_usuarios'),
    path('usuarios/registrar/', views.registro_usuario, name='registro_usuario'),
    path('usuarios/editar/<int:pk>/', views.EditarUsuarioView.as_view(), name='editar_usuario'),
    path('usuarios/eliminar/<int:pk>/', views.EliminarUsuarioView.as_view(), name='eliminar_usuario'),
]