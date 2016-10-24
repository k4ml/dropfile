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

import pytest
import webtest
import cherrypy

from app import get_app

admin_email = 'admin@dropibit.com'

@pytest.fixture(scope='module')
def http():
    db.db.init(':memory:')
    db.db.create_tables([db.User, db.File, db.FileAlias])
    user = db.User.create(email=admin_email)

    cherrypy.config.update({
        'database': db,
        'project_root': config.PROJECT_ROOT,
        'storage_dir': config.STORAGE_DIR,
        'admin_email': admin_email,
    })
    return webtest.TestApp(get_app())

class TestWebAPI(object):
    def test_index(self, http):
        resp = http.get("/")
        assert resp.status_int == 200, resp.status_int

    def test_upload(self, http):
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
        resp = http.post("/api/upload/", b, h)
        assert resp.status_int == 200, resp.status_int
        assert len(resp.json) == 5, resp.json
