from rest_framework.response import Response
from rest_framework.decorators import api_view
from clientes.models import Cliente
from .serializers import ClienteSerializer
from rest_framework.generics import get_object_or_404


@api_view(['GET'])
def getdata(request):
    return Response({"message": "API is working!"})

@api_view(['GET', 'POST'])
def clientes(request):

    if request.method == 'GET':
        clientes = Cliente.objects.all()
        serializer = ClienteSerializer(clientes, many=True)

        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ClienteSerializer(data=request.data)

        if serializer.is_valid():
            cliente = serializer.save()

            return Response(
                ClienteSerializer(cliente).data,
                status=201
            )

        return Response(serializer.errors, status=400)
    
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def get_cliente(request, id):


    if request.method == 'GET':
        cliente = get_object_or_404(Cliente, id=id)
        serializer = ClienteSerializer(cliente)

        return Response(serializer.data)
    
    if request.method in ['PUT', 'PATCH']:
        cliente = get_object_or_404(Cliente, id=id)
        serializer = ClienteSerializer(cliente, data=request.data, partial=(request.method == 'PATCH'))

        if serializer.is_valid():
            cliente = serializer.save()

            return Response(
                ClienteSerializer(cliente).data,
                status=200
            )

        return Response(serializer.errors, status=400)
    
    if request.method == 'DELETE':
        cliente = get_object_or_404(Cliente, id=id)
        cliente.delete()
        return Response(status=204)