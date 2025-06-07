# users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages.views import SuccessMessageMixin

from .forms import CustomUserCreationForm, CustomPasswordResetForm # Importa CustomPasswordResetForm
from django.contrib.auth.forms import PasswordResetForm # Todavía se necesita para la herencia

# --- Vistas existentes ---
@login_required
def home(request):
    """
    Vista de la página de inicio.
    Muestra un mensaje de bienvenida y el nombre de usuario si está logueado.
    """
    return render(request, 'home.html')

class SignUpView(CreateView):
    """
    Vista para el registro de nuevos usuarios.
    Utiliza el formulario CustomUserCreationForm y redirige al login tras el registro exitoso.
    """
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

# --- Vista personalizada para el restablecimiento de contraseña (SOLO PARA DEMO/DESARROLLO) ---
class CustomPasswordResetView(auth_views.PasswordResetView): # No necesitamos SuccessMessageMixin aquí directamente
    """
    Vista personalizada para el restablecimiento de contraseña.
    Utiliza CustomPasswordResetForm para que el enlace se muestre en DEBUG.
    ¡¡¡NO USAR EN PRODUCCIÓN!!!
    """
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    form_class = CustomPasswordResetForm # ¡Usamos nuestro formulario personalizado!

    # Eliminamos el form_valid personalizado aquí, ya que la lógica ahora está en el formulario.
    # El método original de PasswordResetView simplemente llamará a form.save().

# --- NUEVA VISTA PARA EL SEMÁFORO ---
@login_required
def traffic_light_view(request):
    """
    Vista placeholder para el semáforo de consumo eléctrico.
    En la Fase 1, aquí se implementará la lógica para determinar el color.
    """
    # Por ahora, solo un mensaje de placeholder
    context = {
        'current_status': 'Estado actual del semáforo: (Lógica pendiente en Fase 1)',
        'color': 'gray' # Placeholder color
    }
    return render(request, 'traffic_light.html', context)

