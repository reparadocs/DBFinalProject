from MyORM import *
from models import *

db = MyORM('movie')
data_file = open('u.data', 'r')

if not db.doesTableExist(Rating);
  db.createTable(Rating)

for line in data_file:
  data_list = line.split(' ')

  user_id = int(data_list[0])
  movie_id = int(data_list[1])
  i_rating = int(data_list[2])

  rating = Rating([0, user_id, movie_id, i_rating])
  db.insert(rating)
