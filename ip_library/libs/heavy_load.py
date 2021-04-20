import logging
from django.conf import settings
from .extras import LibraryLoader

node_library = None


def load_data():
    global node_library
    logger = logging.getLogger('library_logger')
    try:
        library_path = settings.LIBRARY_PATH
        node_library = LibraryLoader(library_path)\
            .load_library_nodes()
        logger.info('Library file loaded successfully')
    except AttributeError:
        logger.error('No LIBRARY_PATH settings in Django settings file')
    except FileNotFoundError:  
        logger.error('LIBRARY_PATH setting in Django settings is incorect')
