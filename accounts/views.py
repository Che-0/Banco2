
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.template import context
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import LoginForm, RegistroUsuarioForm, EditarUsuarioForm
from .models import User

def es_admin(user):
    return user.is_authenticated and (user.es_admin or user.is_superuser)

# ========== Login / Logout ==========
def login_view(request):
    if request.user.is_authenticated:
        if request.user.es_cliente:
            return redirect('clientes:portal')
        return redirect('core:dashboard')

    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f"Bienvenido, {user.get_full_name() or user.username}")

        if user.es_cliente:
            return redirect('clientes:portal')
        return redirect('core:dashboard')
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('accounts:login')

# ========== Registro de usuarios (solo admin) ==========
@login_required
@user_passes_test(es_admin)
def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Usuario {user.username} creado correctamente.")
            return redirect('accounts:lista_usuarios')
    else:
        form = RegistroUsuarioForm()
    
    return render(request, 'accounts/form_usuario.html', {
    'form': form,
    'titulo': 'Registrar Usuario'
    })

# ========== Listado de usuarios ==========
class ListaUsuariosView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'accounts/lista_usuarios.html'
    context_object_name = 'usuarios'
    paginate_by = 10

    def test_func(self):
        return es_admin(self.request.user)

    def get_queryset(self):
        return User.objects.all().order_by('-date_joined')

# ========== Editar usuario ==========
class EditarUsuarioView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = EditarUsuarioForm
    template_name = 'accounts/form_usuario.html'
    success_url = reverse_lazy('accounts:lista_usuarios')

    def test_func(self):
        return es_admin(self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Usuario actualizado correctamente.")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Usuario'
        return context

# ========== Eliminar usuario ==========
class EliminarUsuarioView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'accounts/eliminar_usuario.html'
    success_url = reverse_lazy('accounts:lista_usuarios')
    context_object_name = 'usuario'

    def test_func(self):
        return es_admin(self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Usuario eliminado correctamente.")
        return super().delete(request, *args, **kwargs)