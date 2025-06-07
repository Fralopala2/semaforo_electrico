# electricity_prices/models.py

from django.db import models
from django.utils import timezone

class ElectricityPrice(models.Model):
    """
    Modelo para almacenar el precio de la electricidad por hora.
    """
    date = models.DateField(default=timezone.now)
    hour = models.IntegerField() # 0-23
    price = models.DecimalField(max_digits=8, decimal_places=5) # Precio en €/kWh
    status = models.CharField(max_length=10, default='unknown') # 'green', 'yellow', 'red'

    class Meta:
        unique_together = ('date', 'hour') # Asegura que solo haya un precio por hora y día
        ordering = ['date', 'hour'] # Ordena por fecha y hora

    def __str__(self):
        return f"{self.date} - {self.hour:02d}h: {self.price} €/kWh ({self.status})"