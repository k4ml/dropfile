import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'lib'))

STORAGE_DIR = os.path.join(PROJECT_ROOT, 'storage')

APP_CONFIG = {
    '/index.html': {
        'tools.staticfile.on': True,
        'tools.staticfile.filename': os.path.join(PROJECT_ROOT, 'public', 'index.html'),
    },
    '/public': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(PROJECT_ROOT, 'public'),
        'tools.staticdir.index': 'index.html',
    },
}
