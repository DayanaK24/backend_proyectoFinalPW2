from django.urls import path
from .views import RegistroAdminEstacionamientoView, LoginAdminEstacionamientoView, EstacionamientoView

urlpatterns = [
    path('registrar/', RegistroAdminEstacionamientoView.as_view(), name='registrar_admin'),
    path('login/', LoginAdminEstacionamientoView.as_view(), name='login_admin'),
    path('estacionamientos/', EstacionamientoView.as_view(), name='crear_estacionamiento'),
    path('estacionamientos/<int:pk>/', EstacionamientoView.as_view(), name='editar_eliminar_estacionamiento'),
]
