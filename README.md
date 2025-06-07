Semáforo Eléctrico

Aplicación web desarrollada con Django y Tailwind CSS para visualizar el precio de la electricidad en España en tiempo real, facilitando la toma de decisiones sobre el consumo energético. La aplicación incluye un sistema de autenticación de usuarios y una interfaz de semáforo que indica el estado del precio.
Descripción
El proyecto "Semáforo Eléctrico" es una herramienta que permite a los usuarios registrados consultar el precio de la electricidad. La información se obtiene de fuentes públicas (OMIE.es) y se presenta de forma visual, utilizando un sistema de semáforo (verde, amarillo, rojo) para indicar momentos óptimos o desfavorables para el consumo.
Características
Autenticación de Usuarios: Registro e inicio de sesión seguro.
Restablecimiento de Contraseña: Funcionalidad para recuperar el acceso a la cuenta.
Visualización del Precio: Interfaz de semáforo simple para el estado actual.
Obtención de Datos: Script para la actualización automática de los precios desde OMIE.es.
Base de Datos: Utiliza PostgreSQL gestionado con Docker Compose.
Diseño Moderno: Interfaz de usuario responsiva y atractiva con Tailwind CSS.
Instalación y Ejecución
Para poner en marcha el proyecto, sigue los siguientes pasos. Se recomienda el uso de una máquina virtual (ej. Debian 12 con VirtualBox) para replicar el entorno de desarrollo.
Prerrequisitos
Asegúrate de tener instalado en tu sistema:
Python 3.x
pip (gestor de paquetes de Python)
Docker Engine (en Linux) o Docker Desktop (en Windows/macOS)
git (para clonar el repositorio)
Pasos de Configuración
Clonar el Repositorio:
git clone https://github.com/tu_usuario/semaforo_electrico.git
cd semaforo_electrico

(Reemplaza https://github.com/tu_usuario/semaforo_electrico.git con la URL real de tu repositorio).
Configurar el Entorno Virtual:
python3 -m venv venv
source venv/bin/activate


Instalar Dependencias de Python:
pip install -r requirements.txt


Configurar Variables de Entorno:
Crea un archivo .env en la raíz del proyecto (junto a manage.py) y añade tus credenciales de base de datos para PostgreSQL. Ejemplo:
DB_NAME=semaforo_db
DB_USER=semaforo_user
DB_PASSWORD=your_db_password
DB_HOST=db
DB_PORT=5432
SECRET_KEY=your_django_secret_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

(Reemplaza your_db_password y your_django_secret_key_here con valores seguros).
Levantar Contenedores Docker (Base de Datos):
Asegúrate de que el servicio Docker está en ejecución y tu usuario tiene permisos.
docker compose up -d

Espera unos segundos (aprox. 10-15) a que la base de datos se inicie completamente.
Aplicar Migraciones de Django:
python manage.py migrate

Obtener Precios de la Electricidad:
Este comando descarga y guarda los precios actuales de OMIE.es en tu base de datos.
python manage.py fetch_prices

(Si no tienes conexión a internet o la fuente está bloqueada, considera la versión de fetch_prices que simula datos para desarrollo).
Inicio Rápido con Alias (Recomendado para uso diario)
Para facilitar el arranque del proyecto, puedes usar un alias en tu terminal.
Asegúrate de que el script start_semaforo.sh existe en tu ~/Escritorio/ (o /home/tu_usuario/Escritorio/). Si no lo tienes, puedes crearlo con el siguiente contenido (reemplazando PROJECT_DIR con la ruta absoluta de tu proyecto):
#!/bin/bash
PROJECT_DIR="/home/paco/projects/semaforo_electrico" # ¡Ajusta esta ruta!
if [ -d "$PROJECT_DIR" ]; then cd "$PROJECT_DIR"; else echo "Error: Proyecto no encontrado."; exit 1; fi
echo "Levantando Docker..."
docker compose up -d || { echo "Error al levantar Docker."; exit 1; }
sleep 10
echo "Activando venv..."
source venv/bin/activate || { echo "Error al activar venv."; exit 1; }
echo "Aplicando migraciones..."
python manage.py migrate || { echo "Advertencia: Migraciones fallidas."; }
echo "Obteniendo precios..."
python manage.py fetch_prices || { echo "Advertencia: Fallo al obtener precios."; }
echo "Iniciando servidor Django..."
nohup python manage.py runserver 0.0.0.0:8000 > django_server.log 2>&1 &
sleep 5
echo "Abriendo navegador..."
xdg-open http://localhost:8000/users/home/
echo "Proyecto iniciado. Logs en django_server.log"

Guarda este archivo como ~/Escritorio/start_semaforo.sh y dale permisos de ejecución: chmod +x ~/Escritorio/start_semaforo.sh.
Crea el alias en tu .bashrc:
nano ~/.bashrc

Añade la siguiente línea al final del archivo:
alias semaforo='bash /home/paco/Escritorio/start_semaforo.sh'

Guarda y cierra (Ctrl+O, Enter, Ctrl+X).
Recarga tu terminal o abre una nueva:
source ~/.bashrc

Ejecutar el proyecto:
Ahora, simplemente escribe en cualquier terminal:
semaforo

Acceso a la Aplicación
Una vez que el servidor Django esté en ejecución, abre tu navegador web y visita:
http://localhost:8000/users/home/
Uso
Registro/Login: Regístrate o inicia sesión para acceder a la funcionalidad del semáforo.
Semáforo de Precios: La sección "Ver Semáforo" mostrará el estado actual del precio de la electricidad (verde/amarillo/rojo) según la lógica implementada.
Restablecimiento de Contraseña (Modo Desarrollo): Si DEBUG=True en settings.py, el enlace de restablecimiento se mostrará directamente en la página de confirmación tras solicitarlo.

Estructura del Proyecto (Simplificada)

![image](https://github.com/user-attachments/assets/bfe0906f-9503-40d5-8467-6bc5b3d6a4f7)


Licencia
Este proyecto está bajo una licencia de uso educativo y no comercial.

Puedes utilizar, modificar y distribuir este software para fines personales o educativos, siempre y cuando no sea para beneficio comercial directo.
Atribución
Si utilizas este proyecto para cualquier propósito (personal, educativo, demostración, etc.), te pido que atribuyas el reconocimiento a su creador:
Paco López Alarte (spanocrypt@gmail.com)
Agradezco tu comprensión y respeto por los términos de uso.
