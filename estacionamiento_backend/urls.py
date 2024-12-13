from django.urls import path, include

urlpatterns = [
    path('api/', include('gestion_estacionamientos.urls')),
]
