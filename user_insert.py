from MyORM import *
from models import *

db = MyORM('movie')

if not db.doesTableExist(User):
  db.createTable(User)

for i in range(1000):
  user = User([0, "User" + str(i+1)])
  db.insert(user)
