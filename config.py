import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'lib'))

import cherrypy

STORAGE_DIR = os.path.join(PROJECT_ROOT, 'storage')

def get_app_config():
    from jinja2 import Environment, FileSystemLoader
    from plugins.jinja2 import TemplatePlugin
    env = Environment(loader=FileSystemLoader(os.path.join(PROJECT_ROOT, 'templates')))
    TemplatePlugin(cherrypy.engine, env=env).subscribe()

    # Register the Jinja2 tool
    from tools.jinja2 import Tool
    cherrypy.tools.template = Tool()
    return {
        '/': {
            'tools.encode.on': False,
        },
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

def get_app(config_=None):
    config_ = config_ or get_app_config()
    from app import Root
    cherrypy.tree.mount(Root(), '/', config_)
    return cherrypy.tree
