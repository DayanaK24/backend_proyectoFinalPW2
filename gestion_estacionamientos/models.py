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
