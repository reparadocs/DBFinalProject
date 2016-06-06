from MyORM import *
from models import *

db = MyORM('movie')
data_file = open('u.data', 'r')

if not db.doesTableExist(Rating):
  db.createTable(Rating)

for line in data_file:
  l = line.split(' ')
  data_list = []
  for it in l:
    if len(it) > 0:
      data_list.append(it)
  user_id = int(data_list[0])
  movie_id = int(data_list[1])
  i_rating = int(data_list[2])

  rating = Rating([0, user_id, movie_id, i_rating])
  db.insert(rating)
