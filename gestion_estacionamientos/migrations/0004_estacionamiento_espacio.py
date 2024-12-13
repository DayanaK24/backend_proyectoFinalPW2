# Generated by Django 5.1.4 on 2024-12-11 10:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_estacionamientos', '0003_adminestacionamiento_delete_usuario'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estacionamiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('ubicacion', models.CharField(max_length=255)),
                ('espacios_totales', models.IntegerField()),
                ('administrador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_estacionamientos.adminestacionamiento')),
            ],
        ),
        migrations.CreateModel(
            name='Espacio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField()),
                ('disponible', models.BooleanField(default=True)),
                ('estacionamiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_estacionamientos.estacionamiento')),
            ],
        ),
    ]