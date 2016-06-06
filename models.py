from MyORM import *

class User(Model):
    username = CharField(100, unique=True)

    def __init__(self, l):
        self.rowid = l[0]
        self.username = l[1]

class Movie(Model):
  title = CharField(300)
  img_link = CharField(500, null=True)

  def __init__(self, l):
    self.rowid = l[0]
    self.title = l[1]

    if len(l) >= 3 and l[2] is not None:
      self.img_link = l[2]
    else:
      self.img_link = None

class Rating(Model):
  user = ForeignKeyField(User)
  movie = ForeignKeyField(Movie)
  rating = IntegerField()

  def __init__(self, l):
    self.rowid = l[0]
    self.user = l[1]
    self.movie = l[2]
    self.rating = l[3]

