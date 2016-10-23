import config

import os
import sys
import unittest

import db
import service

class ServiceTest(unittest.TestCase):
    def setUp(self):
        db.db.init(':memory:')
        db.db.create_tables([db.User, db.File, db.FileAlias])

    def test_save_file(self):
        file_path = 'tests/test_image.jpg'
        file_name = file_path.split('/')[-1]
        test_file1 = open(file_path)
        user = db.User.create(email='me@site.com')

        num_alias = 5
        with db.db.atomic():
            file_ = service.save_file(user, test_file1, num_alias)

        test_file1.close()
        total_alias = file_.aliases.select().count()
        assert total_alias == num_alias, (total_alias, num_alias)
        assert file_.name == file_name, (file_.name, file_name)

import cherrypy
from cherrypy.test import helper

admin_email = 'admin@dropibit.com'
class SimpleCPTest(helper.CPWebCase):
    def setup_server():
        db.db.init(':memory:')
        db.db.create_tables([db.User, db.File, db.FileAlias])
        user = db.User.create(email=admin_email)

        from app import Root
        cherrypy.config.update({
            'database': db,
            'project_root': config.PROJECT_ROOT,
            'storage_dir': config.STORAGE_DIR,
            'admin_email': admin_email,
        })
        cherrypy.tree.mount(Root(), '/', config.APP_CONFIG)
    setup_server = staticmethod(setup_server)

    def setUp(self):
        self.setup_class()

    def tearDown(self):
        self.teardown_class()

    def test_index(self):
        self.getPage("/")
        self.assertStatus('200 OK')
        self.assertHeader('Content-Type', 'text/html;charset=utf-8')

    def test_upload(self):
        # Test upload
        body = '\r\n'.join([
            '--x',
            'Content-Disposition: form-data; name="myfile"; filename="hello.txt"',
            'Content-Type: text/plain',
            '',
            '%s',
            '--x--'])
        partlen = 200 - len(body)
        b = body % ("x" * partlen)
        h = [("Content-type", "multipart/form-data; boundary=x"),
             ("Content-Length", "%s" % len(b))]
        self.getPage("/api/upload/", h, "POST", b)
        self.assertStatus('200 OK')
        self.assertHeader('Content-Type', 'application/json')

if __name__ == '__main__':
    unittest.main()
