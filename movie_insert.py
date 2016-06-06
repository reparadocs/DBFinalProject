import requests
from bs4 import BeautifulSoup
from MyORM import *
from models import *
from unidecode import unidecode

db = MyORM('movie')
data_file = open('u.item', 'r')
save_file = open('links.dat', 'w')

if not db.doesTableExist(Movie):
  db.createTable(Movie)


for line in data_file:
  data_list = line.split('|')
  title = data_list[1]
  title = unicode(title, 'utf-8')
  title = unidecode(title)
  img_url = None
  imdb_url = data_list[4]

  try:
    r = requests.get(imdb_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    poster_class = soup.find('div', {"class":"poster"})
    img_url = poster_class.img['src']
  except:
    movie = Movie([0, title])
    save_file.write(title + '||\n')
    db.insert(movie)
    continue
  img_url = unidecode(img_url)
  movie = Movie([0, title, img_url])
  save_file.write(title + '||' + img_url +'\n')

  db.insert(movie)