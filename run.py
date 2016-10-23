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
import config

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
        'project_root': config.PROJECT_ROOT,
        'storage_dir': config.STORAGE_DIR,
        'admin_email': admin_email,
    })

    cherrypy.tree.mount(Root(), '/', config.APP_CONFIG)
    cherrypy.engine.start()
    cherrypy.engine.block()

@baker.command
def shell():
    import pdb;pdb.set_trace()

if __name__ == '__main__':
    baker.run()
