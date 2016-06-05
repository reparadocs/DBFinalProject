from MyORM import *

class User(Model):
    username = CharField(100)

    def __init__(self, l):
        self.rowid = l[0]
        self.username = l[1]
