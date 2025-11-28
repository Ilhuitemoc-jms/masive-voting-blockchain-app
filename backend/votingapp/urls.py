from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('votos/crear/', views.crear_voto, name='crear_voto'),
    path('votos/', views.obtener_votos, name='obtener_votos'),
    path('health/', views.health_check, name='health_check'),
]
