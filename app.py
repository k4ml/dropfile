import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'lib'))

STORAGE_DIR = os.path.join(PROJECT_ROOT, 'storage')

import cherrypy

class API(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        return {"key": "value"}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def upload(self, myfile):
        filename = os.path.join(STORAGE_DIR, myfile.filename)
        with open(filename, 'wb') as newfile:
            size = 0
            while True:
                data = myfile.file.read(8192)
                if not data:
                    break
                size += len(data)
                newfile.write(data)
        return [
            {'name': 'xxxxx'},
            {'name': 'yyyy'},
        ]

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def list_files(self):
        return [
            {"name": "test.jpg"},
        ]

class Root(object):
    api = API()

    @cherrypy.expose
    def index(self):
        return open(os.path.join(PROJECT_ROOT, 'public', 'index.html')).read()

config = {
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

cherrypy.tree.mount(Root(), '/', config)
cherrypy.engine.start()
cherrypy.engine.block()
