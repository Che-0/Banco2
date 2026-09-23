from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import serializers
from clientes.models import Cliente
from .serializers import ClienteSerializer


@api_view(['GET'])
def getdata(request):
    return Response({"message": "API is working!"})

@api_view(['GET'])
def get_clientes(request):
    clientes = Cliente.objects.all()
    serializer = ClienteSerializer(clientes, many=True)
    return Response(serializer.data)