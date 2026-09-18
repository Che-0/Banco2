from django.contrib import admin
from .models import Cliente, CuentaBancaria

# Register your models here.
admin.site.register(Cliente)
admin.site.register(CuentaBancaria)

