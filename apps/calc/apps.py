from django.apps import AppConfig


class CalcConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'calc'
    verbose_name = 'Расчет цены'
