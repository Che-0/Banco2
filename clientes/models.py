# Create your models here.
from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator, RegexValidator

class Cliente(models.Model):
    class TipoDocumento(models.TextChoices):
        DNI = 'DNI', 'DNI'
        PASAPORTE = 'PASAPORTE', 'Pasaporte'
        OTRO = 'OTRO', 'Otro'

    class Estado(models.TextChoices):
        ACTIVO = 'ACTIVO', 'Activo'
        INACTIVO = 'INACTIVO', 'Inactivo'
        BLOQUEADO = 'BLOQUEADO', 'Bloqueado'

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cliente',
        null=True,
        blank=True
    )

    # Datos personales
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    tipo_documento = models.CharField(
        max_length=20,
        choices=TipoDocumento.choices,
        default=TipoDocumento.DNI
    )
    numero_documento = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    # Dirección
    direccion = models.CharField(max_length=255, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    departamento = models.CharField(max_length=100, blank=True)

    # Estado
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.ACTIVO
    )

    # Auditoría
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='clientes_creados'
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    
    
    foto = models.ImageField(
        upload_to='clientes/fotos/',
        null=True,
        blank=True,
        default='clientes/fotos/default.png',  # imagen por defecto
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])],
        help_text="Foto de perfil del cliente"
    )

    class Meta:
        ordering = ['-fecha_registro']
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.numero_documento}"

    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"

class CuentaBancaria(models.Model):
    class TipoCuenta(models.TextChoices):
        AHORRO = 'AHORRO', 'Cuenta de Ahorro'
        CORRIENTE = 'CORRIENTE', 'Cuenta Corriente'

    class Estado(models.TextChoices):
        ACTIVA = 'ACTIVA', 'Activa'
        INACTIVA = 'INACTIVA', 'Inactiva'
        BLOQUEADA = 'BLOQUEADA', 'Bloqueada'

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='cuentas'
    )
    numero_cuenta = models.CharField(max_length=20, unique=True)
    tipo_cuenta = models.CharField(
        max_length=20,
        choices=TipoCuenta.choices,
        default=TipoCuenta.AHORRO
    )
    saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.ACTIVA
    )
    fecha_apertura = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_apertura']
        verbose_name = 'Cuenta Bancaria'
        verbose_name_plural = 'Cuentas Bancarias'

    def __str__(self):
        return f"{self.numero_cuenta} - {self.cliente.nombre_completo}"
    
    
class Transferencia(models.Model):
    class Tipo(models.TextChoices):
        ENVIADA = 'ENVIADA', 'Enviada'
        RECIBIDA = 'RECIBIDA', 'Recibida'

    class Estado(models.TextChoices):
        COMPLETADA = 'COMPLETADA', 'Completada'
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        RECHAZADA = 'RECHAZADA', 'Rechazada'

    cuenta_origen = models.ForeignKey(
        CuentaBancaria,
        on_delete=models.CASCADE,
        related_name='transferencias_enviadas'
    )
    cuenta_destino = models.ForeignKey(
        CuentaBancaria,
        on_delete=models.CASCADE,
        related_name='transferencias_recibidas'
    )
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    descripcion = models.CharField(max_length=255, blank=True)
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.COMPLETADA
    )
    fecha = models.DateTimeField(auto_now_add=True)
    realizado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Transferencia'
        verbose_name_plural = 'Transferencias'

    def __str__(self):
        return f"{self.cuenta_origen.numero_cuenta} → {self.cuenta_destino.numero_cuenta} | ${self.monto}"