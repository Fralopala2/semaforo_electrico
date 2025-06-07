# electricity_prices/serializers.py

from rest_framework import serializers
from .models import ElectricityPrice # ¡CORREGIDO! Importa ElectricityPrice, no PrecioElectricidad

class ElectricityPriceSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo ElectricityPrice, usado en la API.
    """
    class Meta:
        model = ElectricityPrice
        fields = ['date', 'hour', 'price', 'status']