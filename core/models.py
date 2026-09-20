from django.db import models

# Create your models here.
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

# Esta función "escucha" automáticamente cada vez que alguien hace login
@receiver(user_logged_in)
def notificar_inicio_sesion(sender, user, request, **kwargs):
    # Verificamos que el usuario tenga un correo registrado
    if user.email:
        asunto = 'Alerta de Seguridad: Nuevo inicio de sesión'
        mensaje = f'Hola {user.username},\n\nSe ha detectado un nuevo inicio de sesión en tu cuenta de Banco2. Si no fuiste tú, por favor contacta a soporte de inmediato.'
        remitente = settings.EMAIL_HOST_USER
        destinatarios = [user.email]

        try:
            send_mail(asunto, mensaje, remitente, destinatarios, fail_silently=True)
            print(f"Correo de login enviado a {user.email}")
        except Exception as e:
            print(f"Error al enviar correo de login: {e}")