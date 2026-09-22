import os
import threading
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

# Función auxiliar para enviar el correo en el hilo
def enviar_correo_en_hilo(asunto, mensaje, remitente, destinatarios):
    try:
        send_mail(asunto, mensaje, remitente, destinatarios, fail_silently=False)
        print("Correo enviado exitosamente en segundo plano")
    except Exception as e:
        print(f"Error enviando correo: {e}")

@receiver(user_logged_in)
def notificar_inicio_sesion(sender, user, request, **kwargs):
    if user.email:
        asunto = 'Alerta de Seguridad: Nuevo inicio de sesión'
        mensaje = f'Hola {user.username},\n\nSe ha detectado un nuevo inicio de sesión en tu cuenta de Banco2.'
        
        # Usar None toma directamente settings.DEFAULT_FROM_EMAIL
        remitente = None 
        
        # Obtenemos el correo y lo metemos dentro de una lista [...]
        correo_destino = os.environ.get('EMAIL_RESEND', '').strip()
        
        if not correo_destino:
            print("Aviso: EMAIL_RESEND no está configurado en las variables de entorno.")
            return

        destinatarios = [correo_destino]

        hilo = threading.Thread(
            target=enviar_correo_en_hilo, 
            args=(asunto, mensaje, remitente, destinatarios)
        )
        hilo.start()