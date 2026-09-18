from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

class Notificacion(models.Model):
    class Tipo(models.TextChoices):
        INFO = 'INFO', 'Información'
        EXITO = 'EXITO', 'Éxito'
        ALERTA = 'ALERTA', 'Alerta'
        ERROR = 'ERROR', 'Error'

    destinatario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notificaciones'
    )
    titulo = models.CharField(max_length=150)
    mensaje = models.TextField()
    tipo = models.CharField(
        max_length=20,
        choices=Tipo.choices,
        default=Tipo.INFO
    )
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_lectura = models.DateTimeField(null=True, blank=True)

    # Opcional: enlace a una página específica
    url = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'

    def __str__(self):
        return f"{self.titulo} → {self.destinatario.username}"

    def marcar_como_leida(self):
        if not self.leida:
            from django.utils import timezone
            self.leida = True
            self.fecha_lectura = timezone.now()
            self.save(update_fields=['leida', 'fecha_lectura'])