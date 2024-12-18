from django.db import models
import random
import string

# Generar código único
def generar_codigo():
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(8))

# Modelo Administrador de Estacionamiento
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
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=255)
    espacios_totales = models.IntegerField()
    administrador = models.ForeignKey('AdminEstacionamiento', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    def crear_espacios(self):
        """Crea automáticamente los espacios según la cantidad especificada."""
        Espacio.objects.bulk_create([
            Espacio(numero=i + 1, estacionamiento=self)
            for i in range(self.espacios_totales)
        ])

class Espacio(models.Model):
    numero = models.IntegerField()
    disponible = models.BooleanField(default=True)
    estacionamiento = models.ForeignKey(Estacionamiento, on_delete=models.CASCADE)

    def __str__(self):
        estado = "Disponible" if self.disponible else "Ocupado"
        return f"Espacio {self.numero} ({estado})"

class TipoVehiculo(models.Model):
    tipo = models.CharField(max_length=50)  # Ejemplo: Auto, Moto, Camioneta
    tarifa = models.DecimalField(max_digits=10, decimal_places=2)  # Tarifa en soles
    estacionamiento = models.ForeignKey(Estacionamiento, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tipo} - {self.tarifa} soles"

class RegistroVehiculo(models.Model):
    placa = models.CharField(max_length=20)
    tipo_vehiculo = models.ForeignKey(TipoVehiculo, on_delete=models.CASCADE)
    hora_entrada = models.DateTimeField()
    hora_salida = models.DateTimeField(null=True, blank=True)
    precio_cobrado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE)

    def __str__(self):
        return f"Vehículo {self.placa} - Espacio {self.espacio.numero}"

    def calcular_precio(self):
        if self.hora_salida and self.tipo_vehiculo:
            tiempo = self.hora_salida - self.hora_entrada
            horas = tiempo.total_seconds() / 3600
            self.precio_cobrado = round(horas * float(self.tipo_vehiculo.tarifa), 2)
            self.save()
            
class Incidente(models.Model):
    descripcion = models.TextField()
    fecha_hora = models.DateTimeField(auto_now_add=True)
    estacionamiento = models.ForeignKey(Estacionamiento, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Incidente en {self.estacionamiento.nombre} - {self.fecha_hora}"
