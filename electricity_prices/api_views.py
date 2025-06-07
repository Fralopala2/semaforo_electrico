# electricity_prices/api_views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ElectricityPrice
from .serializers import ElectricityPriceSerializer
from django.utils import timezone
from datetime import datetime, timedelta

class CurrentPriceAPIView(APIView):
    """
    API para obtener el precio actual de la electricidad y su estado.
    """
    def get(self, request, format=None):
        now = timezone.localtime(timezone.now())
        today = now.date()
        current_hour = now.hour

        try:
            # Intenta obtener el precio de la hora actual
            price_data = ElectricityPrice.objects.get(date=today, hour=current_hour)
            serializer = ElectricityPriceSerializer(price_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ElectricityPrice.DoesNotExist:
            # Si no hay datos para la hora actual, intenta obtener los más recientes del día
            # o devuelve un mensaje de error.
            # Aquí, para simplificar, si no hay para la hora exacta,
            # intentamos buscar el último precio disponible del día.
            latest_price = ElectricityPrice.objects.filter(date=today).order_by('-hour').first()
            if latest_price:
                serializer = ElectricityPriceSerializer(latest_price)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": "No hay datos de precios disponibles para hoy."},
                    status=status.HTTP_404_NOT_FOUND
                )

class DailyPricesAPIView(APIView):
    """
    API para obtener todos los precios de la electricidad para un día específico.
    Se puede pasar la fecha como parámetro de consulta (YYYY-MM-DD).
    Si no se pasa, devuelve los precios de hoy.
    """
    def get(self, request, format=None):
        date_str = request.query_params.get('date', None)
        if date_str:
            try:
                target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return Response(
                    {"message": "Formato de fecha inválido. UsaYYYY-MM-DD."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            target_date = timezone.localdate()

        prices = ElectricityPrice.objects.filter(date=target_date)
        serializer = ElectricityPriceSerializer(prices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
