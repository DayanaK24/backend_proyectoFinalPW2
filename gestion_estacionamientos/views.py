from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import AdminEstacionamiento, Estacionamiento, Espacio, TipoVehiculo, RegistroVehiculo, Incidente
from .serializers import AdminEstacionamientoSerializer, EstacionamientoSerializer, TipoVehiculoSerializer, RegistroVehiculoSerializer, IncidenteSerializer

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
        usuario = request.data.get('usuario')
        codigo_unico = request.data.get('codigo_unico')
        accion = request.data.get('accion') 

        if accion != "eliminar":
            return Response({"error": "Acción no permitida. Debes incluir 'eliminar' en la solicitud."}, 
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            admin = AdminEstacionamiento.objects.get(usuario=usuario, codigo_unico=codigo_unico)
            
            estacionamiento = Estacionamiento.objects.get(pk=pk, administrador=admin)
        except AdminEstacionamiento.DoesNotExist:
            return Response({"error": "Administrador no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Estacionamiento.DoesNotExist:
            return Response({"error": "Estacionamiento no encontrado o no pertenece a este administrador."}, 
                            status=status.HTTP_404_NOT_FOUND)

        
        estacionamiento.delete()
        return Response({"message": "Estacionamiento eliminado con éxito."}, status=status.HTTP_200_OK)
    
class ListaEstacionamientosView(APIView):
    def post(self, request):
        usuario = request.data.get('usuario')
        codigo_unico = request.data.get('codigo_unico')

        try:
            
            admin = AdminEstacionamiento.objects.get(usuario=usuario, codigo_unico=codigo_unico)
        except AdminEstacionamiento.DoesNotExist:
            return Response({"error": "Administrador no encontrado."}, status=status.HTTP_404_NOT_FOUND)

       
        estacionamientos = Estacionamiento.objects.filter(administrador=admin)
        serializer = EstacionamientoSerializer(estacionamientos, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

class TipoVehiculoView(APIView):
    def post(self, request):
        usuario = request.data.get('usuario')
        codigo_unico = request.data.get('codigo_unico')
        estacionamiento_id = request.data.get('estacionamiento_id')
        tipo = request.data.get('tipo')
        tarifa = request.data.get('tarifa')

        try:
            admin = AdminEstacionamiento.objects.get(usuario=usuario, codigo_unico=codigo_unico)
            estacionamiento = Estacionamiento.objects.get(id=estacionamiento_id, administrador=admin)
        except AdminEstacionamiento.DoesNotExist:
            return Response({"error": "Administrador no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Estacionamiento.DoesNotExist:
            return Response({"error": "Estacionamiento no encontrado o no pertenece a este administrador."}, 
                            status=status.HTTP_404_NOT_FOUND)

        tipo_vehiculo = TipoVehiculo.objects.create(
            tipo=tipo,
            tarifa=tarifa,
            estacionamiento=estacionamiento
        )

        return Response(TipoVehiculoSerializer(tipo_vehiculo).data, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        usuario = request.data.get('usuario')
        codigo_unico = request.data.get('codigo_unico')

        try:
            admin = AdminEstacionamiento.objects.get(usuario=usuario, codigo_unico=codigo_unico)
            tipo_vehiculo = TipoVehiculo.objects.get(pk=pk, estacionamiento__administrador=admin)
        except (AdminEstacionamiento.DoesNotExist, TipoVehiculo.DoesNotExist):
            return Response({"error": "Tipo de vehículo no encontrado o no pertenece a este administrador."}, 
                            status=status.HTTP_404_NOT_FOUND)

        tipo_vehiculo.tipo = request.data.get('tipo', tipo_vehiculo.tipo)
        tipo_vehiculo.tarifa = request.data.get('tarifa', tipo_vehiculo.tarifa)
        tipo_vehiculo.save()

        return Response(TipoVehiculoSerializer(tipo_vehiculo).data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        usuario = request.data.get('usuario')
        codigo_unico = request.data.get('codigo_unico')

        try:
            admin = AdminEstacionamiento.objects.get(usuario=usuario, codigo_unico=codigo_unico)
            tipo_vehiculo = TipoVehiculo.objects.get(pk=pk, estacionamiento__administrador=admin)
        except (AdminEstacionamiento.DoesNotExist, TipoVehiculo.DoesNotExist):
            return Response({"error": "Tipo de vehículo no encontrado o no pertenece a este administrador."}, 
                            status=status.HTTP_404_NOT_FOUND)

        tipo_vehiculo.delete()
        return Response({"message": "Tipo de vehículo eliminado con éxito."}, status=status.HTTP_200_OK)

from datetime import datetime

class RegistroVehiculoView(APIView):
    def post(self, request):
        usuario = request.data.get('usuario')
        codigo_unico = request.data.get('codigo_unico')
        estacionamiento_id = request.data.get('estacionamiento_id')
        placa = request.data.get('placa')
        tipo_vehiculo_id = request.data.get('tipo_vehiculo_id')
        espacio_id = request.data.get('espacio_id')

        try:
            admin = AdminEstacionamiento.objects.get(usuario=usuario, codigo_unico=codigo_unico)
            estacionamiento = Estacionamiento.objects.get(id=estacionamiento_id, administrador=admin)
            espacio = Espacio.objects.get(id=espacio_id, estacionamiento=estacionamiento, disponible=True)
            tipo_vehiculo = TipoVehiculo.objects.get(id=tipo_vehiculo_id, estacionamiento=estacionamiento)
        except AdminEstacionamiento.DoesNotExist:
            return Response({"error": "Administrador no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Estacionamiento.DoesNotExist:
            return Response({"error": "Estacionamiento no encontrado o no pertenece a este administrador."}, 
                            status=status.HTTP_404_NOT_FOUND)
        except Espacio.DoesNotExist:
            return Response({"error": "Espacio no disponible o no pertenece a este estacionamiento."}, 
                            status=status.HTTP_404_NOT_FOUND)
        except TipoVehiculo.DoesNotExist:
            return Response({"error": "Tipo de vehículo no encontrado o no pertenece a este estacionamiento."}, 
                            status=status.HTTP_404_NOT_FOUND)

        vehiculo = RegistroVehiculo.objects.create(
            placa=placa,
            tipo_vehiculo=tipo_vehiculo,
            hora_entrada=datetime.now(),
            espacio=espacio
        )
        espacio.disponible = False
        espacio.save()

        return Response(RegistroVehiculoSerializer(vehiculo).data, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        usuario = request.data.get('usuario')
        codigo_unico = request.data.get('codigo_unico')

        try:
            admin = AdminEstacionamiento.objects.get(usuario=usuario, codigo_unico=codigo_unico)
            vehiculo = RegistroVehiculo.objects.get(pk=pk, espacio__estacionamiento__administrador=admin)
        except (AdminEstacionamiento.DoesNotExist, RegistroVehiculo.DoesNotExist):
            return Response({"error": "Registro de vehículo no encontrado o no pertenece a este administrador."}, 
                            status=status.HTTP_404_NOT_FOUND)

        vehiculo.placa = request.data.get('placa', vehiculo.placa)
        vehiculo.tipo_vehiculo_id = request.data.get('tipo_vehiculo_id', vehiculo.tipo_vehiculo.id)
        vehiculo.save()

        return Response(RegistroVehiculoSerializer(vehiculo).data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        usuario = request.data.get('usuario')
        codigo_unico = request.data.get('codigo_unico')

        try:
            admin = AdminEstacionamiento.objects.get(usuario=usuario, codigo_unico=codigo_unico)
            vehiculo = RegistroVehiculo.objects.get(pk=pk, espacio__estacionamiento__administrador=admin)
        except (AdminEstacionamiento.DoesNotExist, RegistroVehiculo.DoesNotExist):
            return Response({"error": "Registro de vehículo no encontrado o no pertenece a este administrador."}, 
                            status=status.HTTP_404_NOT_FOUND)

        vehiculo.hora_salida = datetime.now()
        vehiculo.calcular_precio()
        vehiculo.espacio.disponible = True
        vehiculo.espacio.save()

        return Response(RegistroVehiculoSerializer(vehiculo).data, status=status.HTTP_200_OK)

class IncidenteView(APIView):
    def post(self, request):
        usuario = request.data.get('usuario')
        codigo_unico = request.data.get('codigo_unico')
        estacionamiento_id = request.data.get('estacionamiento_id')
        descripcion = request.data.get('descripcion')

        try:
            admin = AdminEstacionamiento.objects.get(usuario=usuario, codigo_unico=codigo_unico)
            estacionamiento = Estacionamiento.objects.get(id=estacionamiento_id, administrador=admin)
        except AdminEstacionamiento.DoesNotExist:
            return Response({"error": "Administrador no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Estacionamiento.DoesNotExist:
            return Response({"error": "Estacionamiento no encontrado o no pertenece a este administrador."}, 
                            status=status.HTTP_404_NOT_FOUND)

        incidente = Incidente.objects.create(
            descripcion=descripcion,
            estacionamiento=estacionamiento
        )

        return Response(IncidenteSerializer(incidente).data, status=status.HTTP_201_CREATED)

    def get(self, request, estacionamiento_id):
        usuario = request.query_params.get('usuario')
        codigo_unico = request.query_params.get('codigo_unico')

        try:
            admin = AdminEstacionamiento.objects.get(usuario=usuario, codigo_unico=codigo_unico)
            estacionamiento = Estacionamiento.objects.get(id=estacionamiento_id, administrador=admin)
        except AdminEstacionamiento.DoesNotExist:
            return Response({"error": "Administrador no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Estacionamiento.DoesNotExist:
            return Response({"error": "Estacionamiento no encontrado o no pertenece a este administrador."}, 
                            status=status.HTTP_404_NOT_FOUND)

        incidentes = Incidente.objects.filter(estacionamiento=estacionamiento)
        return Response(IncidenteSerializer(incidentes, many=True).data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        usuario = request.data.get('usuario')
        codigo_unico = request.data.get('codigo_unico')
        descripcion = request.data.get('descripcion')

        try:
            admin = AdminEstacionamiento.objects.get(usuario=usuario, codigo_unico=codigo_unico)
            incidente = Incidente.objects.get(pk=pk, estacionamiento__administrador=admin)
        except (AdminEstacionamiento.DoesNotExist, Incidente.DoesNotExist):
            return Response({"error": "Incidente no encontrado o no pertenece a este administrador."}, 
                            status=status.HTTP_404_NOT_FOUND)

        incidente.descripcion = descripcion
        incidente.save()

        return Response(IncidenteSerializer(incidente).data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        usuario = request.data.get('usuario')
        codigo_unico = request.data.get('codigo_unico')

        try:
            admin = AdminEstacionamiento.objects.get(usuario=usuario, codigo_unico=codigo_unico)
            incidente = Incidente.objects.get(pk=pk, estacionamiento__administrador=admin)
        except (AdminEstacionamiento.DoesNotExist, Incidente.DoesNotExist):
            return Response({"error": "Incidente no encontrado o no pertenece a este administrador."}, 
                            status=status.HTTP_404_NOT_FOUND)

        incidente.delete()
        return Response({"message": "Incidente eliminado exitosamente."}, status=status.HTTP_200_OK)
