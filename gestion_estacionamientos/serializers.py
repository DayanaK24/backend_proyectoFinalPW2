from rest_framework import serializers
from .models import AdminEstacionamiento, Estacionamiento, Espacio, TipoVehiculo, RegistroVehiculo, Incidente

class AdminEstacionamientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminEstacionamiento
        fields = ['id', 'nombre_completo', 'usuario', 'clave', 'codigo_unico']
        read_only_fields = ['codigo_unico']

class EspacioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Espacio
        fields = ['id', 'disponible']

class EstacionamientoSerializer(serializers.ModelSerializer):
    administrador = AdminEstacionamientoSerializer(read_only=True)
    espacios = EspacioSerializer(many=True, read_only=True)

    class Meta:
        model = Estacionamiento
        fields = ['id', 'espacios_totales', 'administrador', 'espacios']

class TipoVehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoVehiculo
        fields = ['id', 'tipo', 'tarifa_por_hora']

from django.utils import timezone

class RegistroVehiculoSerializer(serializers.ModelSerializer):
    tipo_vehiculo = serializers.PrimaryKeyRelatedField(queryset=TipoVehiculo.objects.all())
    espacio = serializers.PrimaryKeyRelatedField(queryset=Espacio.objects.all())

    class Meta:
        model = RegistroVehiculo
        fields = ['id', 'placa', 'tipo_vehiculo', 'hora_entrada', 'hora_salida', 'precio_cobrado', 'espacio']
        extra_kwargs = {
            'hora_entrada': {'required': False},
        }

    def create(self, validated_data):
        validated_data['hora_entrada'] = timezone.now()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        tipo_vehiculo_data = validated_data.pop('tipo_vehiculo', None)
        espacio_data = validated_data.pop('espacio', None)
        
        if tipo_vehiculo_data:
            tipo_vehiculo = TipoVehiculo.objects.get(id=tipo_vehiculo_data)
            instance.tipo_vehiculo = tipo_vehiculo
        
        if espacio_data:
            espacio = Espacio.objects.get(id=espacio_data)
            instance.espacio = espacio

        if 'hora_entrada' in validated_data:
            instance.hora_entrada = validated_data['hora_entrada']
        
        if 'hora_salida' in validated_data:
            instance.hora_salida = validated_data['hora_salida']
            instance.calcular_precio()
        
        if 'precio_cobrado' in validated_data:
            instance.precio_cobrado = validated_data['precio_cobrado']
        
        instance.save()
        return instance

class IncidenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incidente
        fields = ['id', 'descripcion', 'fecha_hora', 'espacio']
