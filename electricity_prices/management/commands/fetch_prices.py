# electricity_prices/management/commands/fetch_prices.py

from django.core.management.base import BaseCommand
from electricity_prices.models import ElectricityPrice
from django.utils import timezone
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import re # Para expresiones regulares
import io # Para manejar el contenido del archivo como un stream

class Command(BaseCommand):
    help = 'Fetches daily electricity prices from OMIE.es by finding and parsing daily files.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando la captura de precios de electricidad desde OMIE.es (listado de archivos)...'))

        today = timezone.localdate()
        # Formato de fecha para buscar en los nombres de archivo de OMIE (ej. 20250604)
        date_str_file = today.strftime("%Y%m%d")

        # URL de la página de listado de archivos de OMIE.es
        omie_file_list_url = "https://www.omie.es/es/file-access-list?parents=/Mercado%20Diario/1.%20Precios&dir=Precios%20horarios%20del%20mercado%20diario%20en%20Espa%C3%B1a&realdir=marginalpdbc"
        
        try:
            self.stdout.write(f'Accediendo al listado de archivos en: {omie_file_list_url}')
            response = requests.get(omie_file_list_url, verify=False, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            target_file_link = None
            # Patrón de nombre de archivo: marginalpdbc_YYYYMMDD.1
            file_pattern = re.compile(rf"marginalpdbc_{date_str_file}\.1", re.IGNORECASE)

            # Buscar en todos los enlaces de la página
            for link in soup.find_all('a', href=True):
                # OMIE puede tener el nombre del archivo en el texto del enlace o en el atributo href
                if file_pattern.search(link.text) or file_pattern.search(link['href']):
                    # Construir la URL completa del archivo
                    file_path = link['href']
                    if file_path.startswith('/'):
                        # Si es una ruta relativa, asumimos el mismo dominio base
                        base_domain = "https://www.omie.es"
                        target_file_link = f"{base_domain}{file_path}"
                    else:
                        target_file_link = file_path # Si es una URL completa
                    break

            if not target_file_link:
                self.stdout.write(self.style.WARNING(f'No se encontró el enlace al archivo de precios con patrón "marginalpdbc_{date_str_file}.1" para el día {today} en OMIE.es.'))
                self.stdout.write(self.style.WARNING('Puede que los datos del día actual aún no estén publicados o que el patrón del nombre del archivo haya cambiado.'))
                return

            self.stdout.write(f'Encontrado archivo de precios: {target_file_link}')
            self.stdout.write(f'Descargando archivo de precios...')

            # Descargar el archivo de precios
            file_response = requests.get(target_file_link, verify=False, timeout=30)
            file_response.raise_for_status()

            # Leer el contenido del archivo. OMIE suele usar `;` como separador y `,` como decimal.
            # Los precios suelen estar en €/MWh y hay que convertir a €/kWh.
            
            file_content = io.StringIO(file_response.text)
            
            prices_extracted = []
            
            # ¡CORREGIDO! Saltar solo la primera línea que es el encabezado 'MARGINALPDBC;'.
            NUM_HEADER_LINES_TO_SKIP = 1 
            for _ in range(NUM_HEADER_LINES_TO_SKIP):
                file_content.readline()

            for line in file_content:
                line = line.strip()
                if not line:
                    continue # Saltar líneas vacías

                # OMIE suele usar `;` como separador.
                parts = line.split(';')
                
                # ¡CORREGIDO! Ajustar los índices de las partes según el formato proporcionado.
                # Formato: Año;Mes;Día;Hora;Precio1;Precio2;
                if len(parts) >= 5: # Asegurarse de que hay suficientes columnas para Año, Mes, Día, Hora y Precio1
                    try:
                        # La hora está en la cuarta columna (índice 3)
                        hour_str = parts[3].strip()
                        # La hora puede venir como "00" o "00-01". Extraer solo la primera hora.
                        if '-' in hour_str:
                            hour = int(hour_str.split('-')[0].strip())
                        else:
                            hour = int(hour_str)
                        
                        # El precio está en la quinta columna (índice 4)
                        price_mwh_str = parts[4].strip().replace(',', '.')
                        price_mwh = float(price_mwh_str)
                        price_kwh = price_mwh / 1000 # Convertir de €/MWh a €/kWh

                        prices_extracted.append({'hour': hour, 'price': price_kwh})
                    except (ValueError, IndexError) as e:
                        self.stdout.write(self.style.WARNING(f"Saltando línea con formato inesperado o datos inválidos: '{line}' - Error: {e}"))
                        continue
                else:
                    self.stdout.write(self.style.WARNING(f"Saltando línea con número insuficiente de columnas: '{line}'"))


            if not prices_extracted:
                self.stdout.write(self.style.WARNING(f'No se pudieron extraer datos de precios del archivo descargado de OMIE.es para el día {today}.'))
                return

            # Guardar los precios en la base de datos
            for item in prices_extracted:
                hour = item['hour']
                price_value = item['price']

                # --- LÓGICA DEL SEMÁFORO ---
                status = 'unknown' # Estado por defecto
                if price_value < 0.10:
                    status = 'green' # Precio barato
                elif price_value >= 0.10 and price_value < 0.20:
                    status = 'yellow' # Precio normal
                else:
                    status = 'red' # Precio caro

                ElectricityPrice.objects.update_or_create(
                    date=today,
                    hour=hour,
                    defaults={'price': price_value, 'status': status}
                )
                self.stdout.write(f'  Guardado: {today} - {hour:02d}h: {price_value:.5f} €/kWh ({status})')

            self.stdout.write(self.style.SUCCESS('Captura de precios completada con éxito desde OMIE.es.'))

        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Error de red o HTTP al conectar con OMIE.es: {e}'))
            self.stdout.write(self.style.WARNING('Asegúrate de que tienes conexión a internet y que las URLs de OMIE son correctas.'))
        except ValueError as e:
            self.stdout.write(self.style.ERROR(f'Error al parsear los datos de OMIE.es: {e}'))
            self.stdout.write(self.style.WARNING('La estructura de la página de listado o el formato del archivo de OMIE podría haber cambiado. Necesitarás ajustar el código de scraping/parsing.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error inesperado al capturar precios de OMIE.es: {e}'))
            self.stdout.write(self.style.WARNING('Revisa el log para más detalles.'))

        # --- NOTA IMPORTANTE PARA EL USUARIO ---
        # El scraping de sitios web es propenso a fallar si la estructura HTML de la página o el formato de los archivos cambia.
        # Si esta implementación falla, considera usar la simulación de precios o buscar una API
        # más estable (como la de REE/ESIOS si puedes obtener un token en el futuro).
        # ---------------------------------------
