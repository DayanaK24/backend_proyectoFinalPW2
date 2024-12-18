from django.db import models
import random
import string

def generar_codigo():
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(8))

class AdminEstacionamiento(models.Model):
    nombre_completo = models.CharField(max_length=100)
    usuario = models.CharField(max_length=50, unique=True)
    clave = models.CharField(max_length=128)
    codigo_unico = models.CharField(max_length=8, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.codigo_unico:
            self.codigo_unico = generar_codigo()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre_completo

class Estacionamiento(models.Model):
    espacios_totales = models.IntegerField(default=1)

    def __str__(self):
        return f"Estacionamiento - {self.espacios_totales} espacios"

class Espacio(models.Model):
    disponible = models.BooleanField(default=True)

    def __str__(self):
        estado = "Disponible" if self.disponible else "Ocupado"
        return f"Espacio {self.id} ({estado})"

class TipoVehiculo(models.Model):
    tipo = models.CharField(max_length=50)
    tarifa_por_hora = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.tipo} - {self.tarifa_por_hora} soles por hora"

from django.utils import timezone
from decimal import Decimal

class RegistroVehiculo(models.Model):
    placa = models.CharField(max_length=20)
    tipo_vehiculo = models.ForeignKey(TipoVehiculo, on_delete=models.CASCADE)
    hora_entrada = models.DateTimeField()
    hora_salida = models.DateTimeField(null=True, blank=True)
    precio_cobrado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE)

    def __str__(self):
        return f"Vehículo {self.placa} - Espacio {self.espacio.id}"

    def calcular_precio(self):
        if self.hora_salida and self.hora_entrada:
            entrada = timezone.make_aware(self.hora_entrada) if timezone.is_naive(self.hora_entrada) else self.hora_entrada
            salida = timezone.make_aware(self.hora_salida) if timezone.is_naive(self.hora_salida) else self.hora_salida
            tiempo_estacionado = salida - entrada
            horas = Decimal(tiempo_estacionado.total_seconds()) / Decimal(3600) 
            self.precio_cobrado = round(horas * self.tipo_vehiculo.tarifa_por_hora, 2)
            self.save()

class Incidente(models.Model):
    descripcion = models.TextField()
    fecha_hora = models.DateTimeField(auto_now_add=True)
    espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE)

    def __str__(self):
        return f"Incidente en Espacio {self.espacio.id} - {self.fecha_hora}"
