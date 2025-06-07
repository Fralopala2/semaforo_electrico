from django.urls import path
from . import views
from .api_views import CurrentPriceAPIView, DailyPricesAPIView # Importa las vistas de la API

app_name = 'electricity' # ¡NUEVA LÍNEA! Define el nombre de la aplicación para el namespace

urlpatterns = [
    path('traffic-light/', views.traffic_light_display, name='traffic_light'),
    path('api/current/', CurrentPriceAPIView.as_view(), name='api_current_price'),
    path('api/daily/', DailyPricesAPIView.as_view(), name='api_daily_prices'),
]