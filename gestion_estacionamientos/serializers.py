from rest_framework import serializers
from .models import AdminEstacionamiento, Estacionamiento, Espacio

class AdminEstacionamientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminEstacionamiento
        fields = ['id', 'nombre_completo', 'usuario', 'clave', 'codigo_unico']

class EspacioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Espacio
        fields = ['id', 'numero', 'disponible']

class EstacionamientoSerializer(serializers.ModelSerializer):
    espacios = EspacioSerializer(many=True, read_only=True)

    class Meta:
        model = Estacionamiento
        fields = ['id', 'nombre', 'ubicacion', 'espacios_totales', 'espacios', 'administrador']
