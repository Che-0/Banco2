from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Notificacion

class ListaNotificacionesView(LoginRequiredMixin, ListView):
    model = Notificacion
    template_name = 'notificaciones/lista_notificaciones.html'
    context_object_name = 'notificaciones'
    paginate_by = 15

    def get_queryset(self):
        return Notificacion.objects.filter(
            destinatario=self.request.user
        ).order_by('-fecha_creacion')

@login_required
def marcar_como_leida(request, pk):
    notificacion = get_object_or_404(
        Notificacion,
        pk=pk,
        destinatario=request.user
    )
    notificacion.marcar_como_leida()
    messages.success(request, "Notificación marcada como leída.")
    
    # Volver a la página anterior o a la lista
    return redirect(request.META.get('HTTP_REFERER', 'notificaciones:lista'))

@login_required
def marcar_todas_leidas(request):
    Notificacion.objects.filter(
        destinatario=request.user,
        leida=False
    ).update(leida=True, fecha_lectura=timezone.now())
    
    messages.success(request, "Todas las notificaciones fueron marcadas como leídas.")
    return redirect('notificaciones:lista')