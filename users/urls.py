# users/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('signup/', views.SignUpView.as_view(), name='signup'), # URL para el registro
    path('traffic-light/', views.traffic_light_view, name='traffic_light'), # NUEVA URL para el semáforo
]