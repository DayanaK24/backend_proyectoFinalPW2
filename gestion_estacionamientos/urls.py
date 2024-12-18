from django.urls import path
from .views import RegistroAdminEstacionamientoView, LoginAdminEstacionamientoView,CantidadEspaciosView,ListaEspaciosView,EditarEspacioView,ListaTipoVehiculoView,AgregarTipoVehiculoView,EditarTipoVehiculoView,EliminarTipoVehiculoView, ListarVehiculosView, RegistrarVehiculoView, VisualizarVehiculoView,SalidaVehiculoView, ListarIncidentesView, AgregarIncidenteView

urlpatterns = [
    path('registrar/', RegistroAdminEstacionamientoView.as_view(), name='registrar_admin'),
    path('login/', LoginAdminEstacionamientoView.as_view(), name='login_admin'),
    path('cantidad-espacios/', CantidadEspaciosView.as_view(), name='cantidad_espacios'),
    path('lista-espacios/', ListaEspaciosView.as_view(), name='lista_espacios'),
    path('editar-espacio/', EditarEspacioView.as_view(), name='editar_espacio'),
    path('lista-tipo-vehiculo/', ListaTipoVehiculoView.as_view(), name='lista_tipo_vehiculo'),
    path('agregar-tipo-vehiculo/', AgregarTipoVehiculoView.as_view(), name='agregar_tipo_vehiculo'),
    path('editar-tipo-vehiculo/', EditarTipoVehiculoView.as_view(), name='editar_tipo_vehiculo'),
    path('eliminar-tipo-vehiculo/', EliminarTipoVehiculoView.as_view(), name='eliminar_tipo_vehiculo'),path('vehiculos/', ListarVehiculosView.as_view(), name='listar_vehiculos'),
    path('vehiculo/', RegistrarVehiculoView.as_view(), name='registrar_vehiculo'),
    path('vehiculo/<int:pk>/', VisualizarVehiculoView.as_view(), name='visualizar_vehiculo'),
    path('vehiculo/salida/', SalidaVehiculoView.as_view(), name='salida_vehiculo'),
    path('incidentes/', ListarIncidentesView.as_view(), name='listar_incidentes'),
    path('incidentes/agregar/', AgregarIncidenteView.as_view(), name='agregar_incidente'),
    
]


