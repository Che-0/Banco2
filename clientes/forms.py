from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Cliente, CuentaBancaria
from accounts.models import User
import random
import string

class ClienteForm(forms.ModelForm):
    # Campos opcionales para crear usuario
    crear_usuario = forms.BooleanField(
        required=False,
        initial=True,
        label="Crear usuario de acceso",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    username = forms.CharField(
        required=False,
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        required=False,
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        required=False,
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    # Datos de la cuenta bancaria
    tipo_cuenta = forms.ChoiceField(
        choices=CuentaBancaria.TipoCuenta.choices,
        initial=CuentaBancaria.TipoCuenta.AHORRO,
        label="Tipo de cuenta",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    saldo_inicial = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        initial=0,
        label="Saldo inicial",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )

    class Meta:
        model = Cliente
        fields = [
            'nombres', 'apellidos', 'tipo_documento', 'numero_documento',
            'fecha_nacimiento', 'telefono', 'email',
            'direccion', 'ciudad', 'departamento', 'estado'
        ]
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_documento': forms.Select(attrs={'class': 'form-select'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'departamento': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['fecha_nacimiento'].input_formats = ['%Y-%m-%d']
            self.fields['fecha_nacimiento'].widget.attrs.update({
                'type': 'date',
                'class': 'form-control'
        })

    def clean(self):
        cleaned_data = super().clean()
        crear_usuario = cleaned_data.get('crear_usuario')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        username = cleaned_data.get('username')

        if crear_usuario:
            if not username:
                self.add_error('username', 'Debes ingresar un nombre de usuario.')
            if not password1 or not password2:
                self.add_error('password1', 'Debes ingresar una contraseña.')
            if password1 and password2 and password1 != password2:
                self.add_error('password2', 'Las contraseñas no coinciden.')
            if username and User.objects.filter(username=username).exists():
                self.add_error('username', 'Este nombre de usuario ya existe.')
        return cleaned_data

    def generar_numero_cuenta(self):
        """Genera un número de cuenta único de 10 dígitos"""
        while True:
            numero = ''.join(random.choices(string.digits, k=10))
            if not CuentaBancaria.objects.filter(numero_cuenta=numero).exists():
                return numero
            

            
class TransferenciaForm(forms.Form):
    numero_cuenta_destino = forms.CharField(
        label="Número de cuenta destino",
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa el número de cuenta'
        })
    )
    monto = forms.DecimalField(
        label="Monto a transferir",
        max_digits=12,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': '0.00'
        })
    )
    descripcion = forms.CharField(
        label="Descripción (opcional)",
        required=False,
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Pago de servicio'
        })
    )

    def clean_numero_cuenta_destino(self):
        numero = self.cleaned_data['numero_cuenta_destino']
        if not CuentaBancaria.objects.filter(numero_cuenta=numero, estado='ACTIVA').exists():
            raise forms.ValidationError("La cuenta destino no existe o no está activa.")
        return numero
    
class CambiarFotoForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['foto']
        widgets = {
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'foto': 'Nueva foto de perfil',
        }
    
    
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    # Para que el calendario funcione bien al editar
    self.fields['fecha_nacimiento'].input_formats = ['%Y-%m-%d']