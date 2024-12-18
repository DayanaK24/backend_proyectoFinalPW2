from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import AdminEstacionamiento, Estacionamiento, Espacio, TipoVehiculo
from .serializers import AdminEstacionamientoSerializer, EstacionamientoSerializer, TipoVehiculoSerializer

class RegistroAdminEstacionamientoView(APIView):
    def post(self, request):
        serializer = AdminEstacionamientoSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        usuario = serializer.validated_data['usuario']
        if AdminEstacionamiento.objects.filter(usuario=usuario).exists():
            
            return Response(
                {"error": "El usuario ya existe"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        admin = serializer.save()
        data = AdminEstacionamientoSerializer(admin).data
        return Response(data, status=status.HTTP_201_CREATED)

class LoginAdminEstacionamientoView(APIView):
    def post(self, request):
        usuario = request.data.get("usuario")
        clave = request.data.get("clave")
        admin = AdminEstacionamiento.objects.filter(usuario=usuario).first() 
        
        if admin and admin.clave == clave: 
            return Response({"codigo_unico": admin.codigo_unico}, status=status.HTTP_200_OK)
        return Response({"error": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Estacionamiento, Espacio, TipoVehiculo
from .serializers import EstacionamientoSerializer, EspacioSerializer, TipoVehiculoSerializer


class CantidadEspaciosView(APIView):
    def get(self, request):
        estacionamiento = Estacionamiento.objects.first()
        if estacionamiento:
            return Response({"espacios_totales": estacionamiento.espacios_totales})
        return Response({"error": "Estacionamiento no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        estacionamiento = Estacionamiento.objects.first()
        if estacionamiento:
            nueva_cantidad = request.data.get("espacios_totales")
            if nueva_cantidad is not None:
                nueva_cantidad = int(nueva_cantidad)
                espacios_actuales = Espacio.objects.count()

                if nueva_cantidad > espacios_actuales:
                    Espacio.objects.bulk_create([
                        Espacio(disponible=True) for _ in range(nueva_cantidad - espacios_actuales)
                    ])
                elif nueva_cantidad < espacios_actuales:
                    
                    espacios_a_eliminar = Espacio.objects.order_by('-id')[:espacios_actuales - nueva_cantidad]
                    for espacio in espacios_a_eliminar:
                        espacio.delete()

    
                estacionamiento.espacios_totales = nueva_cantidad
                estacionamiento.save()
                return Response({
                    "message": "Cantidad de espacios actualizada correctamente",
                    "espacios_totales": nueva_cantidad
                })

            return Response({"error": "Espacios totales no proporcionados"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Estacionamiento no encontrado"}, status=status.HTTP_404_NOT_FOUND)


class ListaEspaciosView(APIView):
    def get(self, request):
        espacios = Espacio.objects.all()
        return Response(EspacioSerializer(espacios, many=True).data)


class EditarEspacioView(APIView):
    def post(self, request):
        espacio_id = request.data.get("id")
        disponible = request.data.get("disponible")
        if espacio_id is None or disponible is None:
            return Response({"error": "Datos incompletos"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            espacio = Espacio.objects.get(id=espacio_id)
            espacio.disponible = disponible
            espacio.save()
            return Response(EspacioSerializer(espacio).data)
        except Espacio.DoesNotExist:
            return Response({"error": "Espacio no encontrado"}, status=status.HTTP_404_NOT_FOUND)


class ListaTipoVehiculoView(APIView):
    def get(self, request):
        tipos = TipoVehiculo.objects.all()
        return Response(TipoVehiculoSerializer(tipos, many=True).data)


class AgregarTipoVehiculoView(APIView):
    def post(self, request):
        serializer = TipoVehiculoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditarTipoVehiculoView(APIView):
    def post(self, request):
        tipo_id = request.data.get("id")
        if tipo_id is None:
            return Response({"error": "ID del tipo de vehículo no proporcionado"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            tipo_vehiculo = TipoVehiculo.objects.get(id=tipo_id)
            serializer = TipoVehiculoSerializer(tipo_vehiculo, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except TipoVehiculo.DoesNotExist:
            return Response({"error": "Tipo de Vehículo no encontrado"}, status=status.HTTP_404_NOT_FOUND)


class EliminarTipoVehiculoView(APIView):
    def post(self, request):
        tipo_id = request.data.get("id")
        if tipo_id is None:
            return Response({"error": "ID del tipo de vehículo no proporcionado"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            tipo_vehiculo = TipoVehiculo.objects.get(id=tipo_id)
            tipo_vehiculo.delete()
            return Response({"message": "Tipo de Vehículo eliminado"}, status=status.HTTP_204_NO_CONTENT)
        except TipoVehiculo.DoesNotExist:
            return Response({"error": "Tipo de Vehículo no encontrado"}, status=status.HTTP_404_NOT_FOUND)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RegistroVehiculo, Espacio, TipoVehiculo
from .serializers import RegistroVehiculoSerializer

class ListarVehiculosView(APIView):
    def get(self, request):
        vehiculos = RegistroVehiculo.objects.all()
        serializer = RegistroVehiculoSerializer(vehiculos, many=True)
        return Response(serializer.data)

class RegistrarVehiculoView(APIView):
    def post(self, request):
        serializer = RegistroVehiculoSerializer(data=request.data)
        if serializer.is_valid():
            espacio = serializer.validated_data['espacio']
            if not espacio.disponible:
                return Response({"error": "El espacio no está disponible."}, status=status.HTTP_400_BAD_REQUEST)

            espacio.disponible = False
            espacio.save()

            registro = serializer.save()
            return Response(RegistroVehiculoSerializer(registro).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RegistroVehiculo, Espacio
from .serializers import RegistroVehiculoSerializer
from datetime import datetime

from django.utils import timezone

class SalidaVehiculoView(APIView):
    def post(self, request):
        registro_id = request.data.get("registro_id")

        try:
            registro = RegistroVehiculo.objects.get(id=registro_id)
        except RegistroVehiculo.DoesNotExist:
            return Response({"error": "Registro no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        if registro.hora_salida is not None:
            return Response({"error": "El vehículo ya ha marcado su salida"}, status=status.HTTP_400_BAD_REQUEST)

        registro.hora_salida = timezone.now()
        registro.calcular_precio()

        espacio = registro.espacio
        espacio.disponible = True
        espacio.save()

        return Response(RegistroVehiculoSerializer(registro).data, status=status.HTTP_200_OK)


class VisualizarVehiculoView(APIView):
    def get(self, request, pk):
        try:
            vehiculo = RegistroVehiculo.objects.get(pk=pk)
            serializer = RegistroVehiculoSerializer(vehiculo)
            return Response(serializer.data)
        except RegistroVehiculo.DoesNotExist:
            return Response({"error": "Vehículo no encontrado."}, status=status.HTTP_404_NOT_FOUND)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Incidente, Espacio
from .serializers import IncidenteSerializer

class ListarIncidentesView(APIView):
    def get(self, request):
        incidentes = Incidente.objects.all()
        serializer = IncidenteSerializer(incidentes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AgregarIncidenteView(APIView):
    def post(self, request):
        serializer = IncidenteSerializer(data=request.data)
        if serializer.is_valid():
            espacio_id = serializer.validated_data.get('espacio').id
            try:
                espacio = Espacio.objects.get(id=espacio_id)
                if not espacio.disponible:
                    return Response({"error": "No se puede registrar un incidente en un espacio ocupado."}, status=status.HTTP_400_BAD_REQUEST)
                incidente = serializer.save()
                return Response(IncidenteSerializer(incidente).data, status=status.HTTP_201_CREATED)
            except Espacio.DoesNotExist:
                return Response({"error": "Espacio no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
