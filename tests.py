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

unittest.main()
