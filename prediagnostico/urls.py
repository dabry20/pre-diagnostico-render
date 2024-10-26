from django.urls import path
from prediagnostico import views
urlpatterns = [
    path('',views.login, name="login"),
    path('home/',views.home, name="Home"),
    path('registro/',views.registro, name="Registro"),
    
    path('editar_paciente/', views.Editar_paciente, name='Editar_paciente'),
    path('vista/',views.vista, name="Vista"),
    path('recuperar/',views.recuperar, name="Recuperar"),
    path('restablecer/<uuid:token>/',views.restablecer, name="Restablecer"),
    path('historia',views.historial, name="Historial"),
]