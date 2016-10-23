"""
Copyright 2016 Kamal Mustafa

This file is part of Dropibit.

Dropibit is free software: you can redistribute it and/or modify
it under the terms of the Afferor GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Dropibit is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the Affero GNU General Public License
along with Dropibit.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'lib'))

STORAGE_DIR = os.path.join(PROJECT_ROOT, 'storage')

import db
import service

import baker
import cherrypy

from app import Root

@baker.command
def app(admin_email=None):
    if admin_email is None:
        admin_email = os.environ['ADMIN_EMAIL']

    db.db.init('dropibit.db')
    cherrypy.config.update({
        'database': db,    
        'project_root': PROJECT_ROOT,
        'storage_dir': STORAGE_DIR,
        'admin_email': admin_email,
    })

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

@baker.command
def shell():
    import pdb;pdb.set_trace()

if __name__ == '__main__':
    baker.run()
