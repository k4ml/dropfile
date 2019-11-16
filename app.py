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

import cherrypy

class API(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        return {"key": "value"}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def upload(self, myfile):
        storage_dir = cherrypy.config['storage_dir']
        admin_email = cherrypy.config['admin_email']
        db = cherrypy.config['database']

        ext = myfile.filename.split('.')[-1]
        filename = os.path.join(storage_dir,
                                '%s.%s' % (service.id_generator(), ext))

        with open(filename, 'wb') as newfile:
            size = 0
            while True:
                data = myfile.file.read(8192)
                if not data:
                    break
                size += len(data)
                newfile.write(data)

            if size > 0:
                user = db.User.get(email=admin_email)
                file_ = service.save_file(user, newfile)
                out = []
                for alias in file_.aliases.select().limit(5):
                    out.append({
                        'name': alias.alias,
                    })

                return out

        return []

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def list_files(self):
        return [
            {"name": "test.jpg"},
        ]

class Root(object):
    api = API()

    @cherrypy.expose
    @cherrypy.tools.template(template='base.html')
    def index(self):
        project_root = cherrypy.config['project_root']
        return {
            'name': 'test',
        }
