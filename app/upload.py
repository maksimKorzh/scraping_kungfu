import pymongo
import csv, json

client = pymongo.MongoClient('mongodb+srv://cmk:342124@todolist-c483l.gcp.mongodb.net/scraping_kungfu?retryWrites=true&w=majority')    
db = client.scraping_kungfu

data = []

with open('movies.csv', 'r') as csv_file:
    reader= csv.DictReader(csv_file)
    
    for entry in reader:
        data.append(entry)

movies = db.movies
movies.insert_many(data)
movies.create_index([
    ('title', pymongo.TEXT),
    ('country', pymongo.TEXT),
    ('release_year', pymongo.TEXT),
    ('genre', pymongo.TEXT),
    ('director', pymongo.TEXT),
    ('starring', pymongo.TEXT)
], name='search_movies', default_language='english')



