import random
import string

from db import File, FileAlias

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def save_file(user, myfile, num_alias=5):
    file_ = File(name=myfile.name, user=user)
    file_.save()

    for i in range(num_alias):
        filealias = FileAlias(alias=id_generator(), file_=file_)
        print(filealias.alias)
        filealias.save()

    return file_
