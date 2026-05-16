from django.apps import AppConfig



class MerchantsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.merchants'
    verbose_name = 'Merchant Management'

    def ready(self):
        from . import signals