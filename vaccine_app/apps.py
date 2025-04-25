from django.apps import AppConfig

class VaccineAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vaccine_app'

    def ready(self):
        from .scheduler import start_scheduler
        start_scheduler()
