from rest_framework import serializers
from clientes.models import Cliente


class ClienteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cliente

        fields = [
            'id',
            'nombres',
            'apellidos',
            'tipo_documento',
            'numero_documento',
            'fecha_nacimiento',
            'telefono',
            'email',
            'direccion',
            'ciudad',
            'departamento',
            'estado',
            'foto',
            'fecha_registro',
            'actualizado',
        ]

        read_only_fields = [
            'id',
            'fecha_registro',
            'actualizado',
        ]