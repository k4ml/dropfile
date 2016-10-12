import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'lib'))

import cherrypy

class Root(object):
    @cherrypy.expose
    def index(self):
        return open(os.path.join(PROJECT_ROOT, 'public', 'index.html')).read()

class API(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        return {"key": "value"}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def upload(self, myfile):
        with open('newfile.upload', 'wb') as newfile:
            size = 0
            while True:
                data = myfile.file.read(8192)
                if not data:
                    break
                size += len(data)
                newfile.write(data)
        return {"status": size}

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
cherrypy.tree.mount(API(), '/api', config)
cherrypy.engine.start()
cherrypy.engine.block()
