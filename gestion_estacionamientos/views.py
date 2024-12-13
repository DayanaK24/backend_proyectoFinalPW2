from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import AdminEstacionamiento, Estacionamiento, Espacio
from .serializers import AdminEstacionamientoSerializer, EstacionamientoSerializer

class RegistroAdminEstacionamientoView(APIView):
    def post(self, request):
        serializer = AdminEstacionamientoSerializer(data=request.data)
        if serializer.is_valid():
            if AdminEstacionamiento.objects.filter(usuario=serializer.validated_data['usuario']).exists():
                return Response({"error": "El usuario ya existe"}, status=status.HTTP_400_BAD_REQUEST)
            admin = serializer.save()
            return Response(AdminEstacionamientoSerializer(admin).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAdminEstacionamientoView(APIView):
    def post(self, request):
        usuario = request.data.get("usuario")
        clave = request.data.get("clave")
        admin = AdminEstacionamiento.objects.filter(usuario=usuario).first() 
        
        if admin and admin.clave == clave: 
            return Response({"codigo_unico": admin.codigo_unico}, status=status.HTTP_200_OK)
        return Response({"error": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)


class EstacionamientoView(APIView):
    def post(self, request):
        """Crear un nuevo estacionamiento."""
        usuario = request.data.get('usuario')
        codigo_unico = request.data.get('codigo_unico')
        nombre = request.data.get('nombre')
        ubicacion = request.data.get('ubicacion')
        espacios_totales = request.data.get('espacios_totales')

        try:
            admin = AdminEstacionamiento.objects.get(usuario=usuario, codigo_unico=codigo_unico)
        except AdminEstacionamiento.DoesNotExist:
            return Response({"error": "Usuario o código único inválido."}, status=status.HTTP_404_NOT_FOUND)

        estacionamiento = Estacionamiento(
            nombre=nombre,
            ubicacion=ubicacion,
            espacios_totales=espacios_totales,
            administrador=admin
        )
        estacionamiento.save()
        estacionamiento.crear_espacios() 

        return Response(EstacionamientoSerializer(estacionamiento).data, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        """Editar un estacionamiento existente."""
        usuario = request.data.get('usuario')
        codigo_unico = request.data.get('codigo_unico')
        try:
            admin = AdminEstacionamiento.objects.get(usuario=usuario, codigo_unico=codigo_unico)
            estacionamiento = Estacionamiento.objects.get(pk=pk, administrador=admin)
        except (AdminEstacionamiento.DoesNotExist, Estacionamiento.DoesNotExist):
            return Response({"error": "Estacionamiento o administrador no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        estacionamiento.nombre = request.data.get('nombre', estacionamiento.nombre)
        estacionamiento.ubicacion = request.data.get('ubicacion', estacionamiento.ubicacion)
        estacionamiento.espacios_totales = request.data.get('espacios_totales', estacionamiento.espacios_totales)
        estacionamiento.save()

        return Response(EstacionamientoSerializer(estacionamiento).data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        """Eliminar un estacionamiento existente basado en usuario, código único y palabra clave 'eliminar'."""
        usuario = request.data.get('usuario')
        codigo_unico = request.data.get('codigo_unico')
        accion = request.data.get('accion')  # Validar la palabra clave 'eliminar'

        # Verificar que se incluyó la palabra clave 'eliminar'
        if accion != "eliminar":
            return Response({"error": "Acción no permitida. Debes incluir 'eliminar' en la solicitud."}, 
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # Verificar que el administrador existe
            admin = AdminEstacionamiento.objects.get(usuario=usuario, codigo_unico=codigo_unico)
            # Verificar que el estacionamiento pertenece al administrador
            estacionamiento = Estacionamiento.objects.get(pk=pk, administrador=admin)
        except AdminEstacionamiento.DoesNotExist:
            return Response({"error": "Administrador no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Estacionamiento.DoesNotExist:
            return Response({"error": "Estacionamiento no encontrado o no pertenece a este administrador."}, 
                            status=status.HTTP_404_NOT_FOUND)

        # Eliminar el estacionamiento
        estacionamiento.delete()
        return Response({"message": "Estacionamiento eliminado con éxito."}, status=status.HTTP_200_OK)