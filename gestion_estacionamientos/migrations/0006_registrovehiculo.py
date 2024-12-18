# Generated by Django 5.1.4 on 2024-12-18 01:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_estacionamientos', '0005_tipovehiculo'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistroVehiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placa', models.CharField(max_length=20)),
                ('hora_entrada', models.DateTimeField()),
                ('hora_salida', models.DateTimeField(blank=True, null=True)),
                ('precio_cobrado', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('espacio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_estacionamientos.espacio')),
                ('tipo_vehiculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_estacionamientos.tipovehiculo')),
            ],
        ),
    ]
