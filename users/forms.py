# users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
import logging

logger = logging.getLogger(__name__)

# Formulario de registro personalizado
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-input'
            })

# Formulario de login personalizado
class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Tu nombre de usuario'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Tu contraseña'
        })

# --- Formulario de restablecimiento de contraseña personalizado (SOLO PARA DEMO/DESARROLLO) ---
class CustomPasswordResetForm(PasswordResetForm):
    """
    Formulario de restablecimiento de contraseña que, en modo DEBUG,
    guarda el enlace de restablecimiento en la sesión para mostrarlo directamente en la página.
    ¡¡¡NO USAR EN PRODUCCIÓN!!!
    """
    # Importante: Añadir **kwargs para aceptar todos los argumentos pasados por la vista padre
    def save(self, domain_override=None, subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None, **kwargs): # Añadido **kwargs

        # Llama al método save original de PasswordResetForm, pasando todos los kwargs
        super_return = super().save(
            domain_override=domain_override,
            subject_template_name=subject_template_name,
            email_template_name=email_template_name,
            use_https=use_https,
            token_generator=token_generator,
            from_email=from_email,
            request=request,
            html_email_template_name=html_email_template_name,
            **kwargs # ¡Pasa los kwargs a la función padre!
        )

        # Si estamos en modo DEBUG y tenemos la request (para acceder a la sesión)
        if settings.DEBUG and request:
            try:
                # Intentamos reconstruir el enlace para mostrarlo directamente
                email = self.cleaned_data["email"]
                # Obtener el usuario del formulario validado
                # get_users_and_attrs es un método interno, no lo usamos directamente
                # Iteramos sobre los usuarios que coinciden con el email
                for user in User._default_manager.filter(email__iexact=email, is_active=True):
                    if user.has_usable_password(): # Solo si tiene contraseña usable (no externo)
                        current_site = get_current_site(request)
                        uid = urlsafe_base64_encode(force_bytes(user.pk))
                        token = token_generator.make_token(user)
                        reset_url = request.build_absolute_uri(
                            reverse_lazy('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                        )
                        request.session['password_reset_debug_url'] = reset_url
                        request.session['password_reset_debug_user'] = user.username
                        logger.info(f"DEBUG: Enlace de restablecimiento generado para {user.username}: {reset_url}")
                        break # Encontramos un usuario, no necesitamos seguir buscando
            except Exception as e:
                logger.error(f"Error al capturar el enlace de restablecimiento en DEBUG: {e}")
                # Limpiar la sesión si hubo un error para no mostrar info incorrecta
                if 'password_reset_debug_url' in request.session:
                    del request.session['password_reset_debug_url']
                if 'password_reset_debug_user' in request.session:
                    del request.session['password_reset_debug_user']

        return super_return

