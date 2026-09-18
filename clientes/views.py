
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Cliente, CuentaBancaria, Transferencia
from .forms import ClienteForm, TransferenciaForm
from accounts.models import User
from notificaciones.models import Notificacion
from .forms import ClienteForm, TransferenciaForm, CambiarFotoForm


from decimal import Decimal
from django.db import transaction

def es_admin_o_empleado(user):
    return user.is_authenticated and (user.es_admin or user.es_empleado or user.is_superuser)

# ========== Listado de clientes ==========
class ListaClientesView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Cliente
    template_name = 'clientes/lista_clientes.html'
    context_object_name = 'clientes'
    paginate_by = 10

    def test_func(self):
        return es_admin_o_empleado(self.request.user)

    def get_queryset(self):
        queryset = Cliente.objects.select_related('usuario', 'creado_por').all()
        # Filtro simple por búsqueda
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                models.Q(nombres__icontains=q) |
                models.Q(apellidos__icontains=q) |
                models.Q(numero_documento__icontains=q)
            )
        return queryset

# Necesitas importar models para el Q
from django.db import models

# ========== Crear cliente ==========
@login_required
@login_required
@user_passes_test(es_admin_o_empleado)
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.creado_por = request.user

            # Crear usuario si se solicitó
            if form.cleaned_data.get('crear_usuario'):
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password1'],
                    first_name=form.cleaned_data['nombres'],
                    last_name=form.cleaned_data['apellidos'],
                    email=form.cleaned_data.get('email', ''),
                    telefono=form.cleaned_data.get('telefono', ''),
                    rol=User.Rol.CLIENTE
                )
                cliente.usuario = user

            cliente.save()

            # Crear cuenta bancaria automáticamente
            CuentaBancaria.objects.create(
                cliente=cliente,
                numero_cuenta=form.generar_numero_cuenta(),
                tipo_cuenta=form.cleaned_data['tipo_cuenta'],
                saldo=form.cleaned_data['saldo_inicial'],
                estado=CuentaBancaria.Estado.ACTIVA
            )

            # Notificación
            Notificacion.objects.create(
                destinatario=request.user,
                titulo="Cliente registrado",
                mensaje=f"Se registró al cliente {cliente.nombre_completo} con su cuenta bancaria.",
                tipo=Notificacion.Tipo.EXITO
            )

            messages.success(request, f"Cliente {cliente.nombre_completo} y su cuenta fueron creados correctamente.")
            return redirect('clientes:lista_clientes')
    else:
        form = ClienteForm()

    return render(request, 'clientes/form_cliente.html', {
        'form': form,
        'titulo': 'Registrar Cliente + Cuenta'
    })

# ========== Detalle de cliente ==========
class DetalleClienteView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Cliente
    template_name = 'clientes/detalle_cliente.html'
    context_object_name = 'cliente'

    def test_func(self):
        return es_admin_o_empleado(self.request.user)

# ========== Editar cliente ==========
class EditarClienteView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/form_cliente.html'
    success_url = reverse_lazy('clientes:lista_clientes')

    def test_func(self):
        return es_admin_o_empleado(self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Cliente actualizado correctamente.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Cliente'
        return context

# ========== Eliminar cliente ==========
class EliminarClienteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Cliente
    template_name = 'clientes/eliminar_cliente.html'
    success_url = reverse_lazy('clientes:lista_clientes')
    context_object_name = 'cliente'

    def test_func(self):
        return es_admin_o_empleado(self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Cliente eliminado correctamente.")
        return super().delete(request, *args, **kwargs)
    
    
@login_required
def portal_cliente(request):
    # Solo los clientes pueden entrar aquí
    if not hasattr(request.user, 'rol') or request.user.rol != 'CLIENTE':
        messages.warning(request, "Esta sección es solo para clientes.")
        return redirect('core:dashboard')

    try:
        cliente = request.user.cliente
        cuenta = cliente.cuentas.filter(estado='ACTIVA').first()
    except Exception:
        messages.error(request, "No tienes un perfil de cliente asociado.")
        return redirect('core:dashboard')   # Mejor que cerrar sesión

    transferencias = []
    if cuenta:
        transferencias = Transferencia.objects.filter(
            models.Q(cuenta_origen=cuenta) | models.Q(cuenta_destino=cuenta)
        ).order_by('-fecha')[:10]

    context = {
        'cliente': cliente,
        'cuenta': cuenta,
        'transferencias': transferencias,
    }
    return render(request, 'clientes/portal_cliente.html', context)

@login_required
def realizar_transferencia(request):
    if not request.user.es_cliente:
        return redirect('core:dashboard')

    cliente = request.user.cliente
    cuenta_origen = cliente.cuentas.filter(estado='ACTIVA').first()

    if not cuenta_origen:
        messages.error(request, "No tienes una cuenta activa.")
        return redirect('clientes:portal')

    if request.method == 'POST':
        form = TransferenciaForm(request.POST)
        if form.is_valid():
            numero_destino = form.cleaned_data['numero_cuenta_destino']
            monto = form.cleaned_data['monto']
            descripcion = form.cleaned_data['descripcion']

            cuenta_destino = CuentaBancaria.objects.get(numero_cuenta=numero_destino)

            if cuenta_destino == cuenta_origen:
                messages.error(request, "No puedes transferir a tu misma cuenta.")
                return redirect('clientes:transferencia')

            if cuenta_origen.saldo < monto:
                messages.error(request, "Saldo insuficiente.")
                return redirect('clientes:transferencia')

            # Realizar la transferencia de forma segura
            with transaction.atomic():
                cuenta_origen.saldo -= monto
                cuenta_origen.save()

                cuenta_destino.saldo += monto
                cuenta_destino.save()

                Transferencia.objects.create(
                    cuenta_origen=cuenta_origen,
                    cuenta_destino=cuenta_destino,
                    monto=monto,
                    descripcion=descripcion,
                    realizado_por=request.user
                )

                # Notificaciones
                Notificacion.objects.create(
                    destinatario=request.user,
                    titulo="Transferencia realizada",
                    mensaje=f"Enviaste ${monto} a la cuenta {numero_destino}.",
                    tipo=Notificacion.Tipo.EXITO
                )
                if cuenta_destino.cliente.usuario:
                    Notificacion.objects.create(
                        destinatario=cuenta_destino.cliente.usuario,
                        titulo="Transferencia recibida",
                        mensaje=f"Recibiste ${monto} de la cuenta {cuenta_origen.numero_cuenta}.",
                        tipo=Notificacion.Tipo.INFO
                    )

            messages.success(request, f"Transferencia de ${monto} realizada con éxito.")
            return redirect('clientes:portal')
    else:
        form = TransferenciaForm()

    return render(request, 'clientes/realizar_transferencia.html', {
        'form': form,
        'cuenta': cuenta_origen
    })
    
@login_required
def cambiar_foto(request):
    if not request.user.es_cliente:
        return redirect('core:dashboard')

    cliente = request.user.cliente

    if request.method == 'POST':
        form = CambiarFotoForm(request.POST, request.FILES, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, "Foto actualizada correctamente.")
            return redirect('clientes:portal')
    else:
        form = CambiarFotoForm(instance=cliente)

    return render(request, 'clientes/cambiar_foto.html', {
        'form': form,
        'cliente': cliente
    })