from django.apps import AppConfig

# ELR: Clase de configuración para recursos en la carpeta 'app_notes'.
#      Esto es referenciado en 'settings.py' para cargarlo en arranque de framework.
class AppNotesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_notes'
