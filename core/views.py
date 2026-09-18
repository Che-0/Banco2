from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from clientes.models import Cliente
from accounts.models import User
from notificaciones.models import Notificacion
from django.shortcuts import redirect

@login_required
def dashboard(request):
    # Los clientes no deben ver este dashboard
    if request.user.es_cliente:
        return redirect('clientes:portal')

    context = {
        'total_clientes': Cliente.objects.count(),
        'total_usuarios': User.objects.count(),
        'clientes_recientes': Cliente.objects.order_by('-fecha_registro')[:5],
        'notificaciones_recientes': Notificacion.objects.filter(
            destinatario=request.user
        ).order_by('-fecha_creacion')[:5],
    }
    return render(request, 'core/dashboard.html', context)