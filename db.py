
from peewee import *

db = SqliteDatabase(None)

class MyModel(Model):
    class Meta:
        database = db

class User(MyModel):
    email = CharField(unique=True)

class File(MyModel):
    name = CharField(unique=True)
    user = ForeignKeyField(User)

class FileAlias(MyModel):
    alias = CharField(unique=True)
    file_ = ForeignKeyField(File, related_name='aliases')
