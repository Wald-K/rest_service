import logging
from django.apps import AppConfig
from .libs.heavy_load import load_data


logger = logging.getLogger('library_logger')


class IpLibraryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ip_library'

    def ready(self):
        load_data()
