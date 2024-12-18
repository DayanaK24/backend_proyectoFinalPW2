from django.urls import path
from .views import RegistroAdminEstacionamientoView, LoginAdminEstacionamientoView, EstacionamientoView,ListaEstacionamientosView,  TipoVehiculoView, RegistroVehiculoView, IncidenteView

urlpatterns = [
    path('registrar/', RegistroAdminEstacionamientoView.as_view(), name='registrar_admin'),
    path('login/', LoginAdminEstacionamientoView.as_view(), name='login_admin'),
    path('estacionamientos/', EstacionamientoView.as_view(), name='crear_estacionamiento'),
    path('estacionamientos/<int:pk>/', EstacionamientoView.as_view(), name='editar_eliminar_estacionamiento'),
    path('estacionamientos/listar/', ListaEstacionamientosView.as_view(), name='listar_estacionamientos'),
    path('tipo-vehiculo/', TipoVehiculoView.as_view(), name='agregar_tipo_vehiculo'),
    path('tipo-vehiculo/<int:pk>/', TipoVehiculoView.as_view(), name='editar_eliminar_tipo_vehiculo'),
    path('vehiculos/', RegistroVehiculoView.as_view(), name='registrar_vehiculo'),
    path('vehiculos/<int:pk>/', RegistroVehiculoView.as_view(), name='editar_vehiculo'),
    path('vehiculos/salida/<int:pk>/', RegistroVehiculoView.as_view(), name='registrar_salida_vehiculo'),
     path('incidentes/', IncidenteView.as_view(), name='registrar_incidente'),
    path('incidentes/<int:estacionamiento_id>/', IncidenteView.as_view(), name='listar_incidentes'),
    path('incidentes/editar/<int:pk>/', IncidenteView.as_view(), name='editar_incidente'),
    path('incidentes/eliminar/<int:pk>/', IncidenteView.as_view(), name='eliminar_incidente'),

]


