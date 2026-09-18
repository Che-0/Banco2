
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Rol(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'
        EMPLEADO = 'EMPLEADO', 'Empleado'
        CLIENTE = 'CLIENTE', 'Cliente'

    rol = models.CharField(
        max_length=20,
        choices=Rol.choices,
        default=Rol.CLIENTE
    )
    telefono = models.CharField(max_length=20, blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.username}) - {self.get_rol_display()}"

    @property
    def es_admin(self):
        return self.rol == self.Rol.ADMIN or self.is_superuser

    @property
    def es_empleado(self):
        return self.rol == self.Rol.EMPLEADO

    @property
    def es_cliente(self):
        return self.rol == self.Rol.CLIENTE