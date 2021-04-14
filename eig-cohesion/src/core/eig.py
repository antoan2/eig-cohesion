import hashlib

class Eig:
    def __init__(self, name: str, project: str):
        self.name = name
        self.project = project
    
    def __repr__(self):
        return ' - '.join((self.project, self.name))

    def get_hash(self):
        hash_object = hashlib.md5((self.name + self.project).encode())
        return hash_object.hexdigest()