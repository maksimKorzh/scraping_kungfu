######################################################
# 
# Libraries
#
######################################################

from flask import Flask
from flask import request
from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
from flask_pymongo import PyMongo
from flask_paginate import Pagination, get_page_args


######################################################
# 
# App instance & config
#
######################################################

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://cmk:342124@todolist-c483l.gcp.mongodb.net/scraping_kungfu?retryWrites=true&w=majority"
mongo = PyMongo(app)


######################################################
# 
# Routes
#
######################################################

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/chamber_1')
def first_chamber():
    movie = mongo.db.movies.find_one({'title': 'The 36th Chamber of Shaolin'})
    return render_template('chamber_1.html', movie=movie)

@app.route('/chamber_2')
def second_chamber():
    movies = mongo.db.movies.find(limit=50)
    return render_template('chamber_2.html', movies=movies)

@app.route('/chamber_3')
def third_chamber():
    movies = [movie for movie in mongo.db.movies.find()]
    total = len(movies)
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    
    return render_template('chamber_3.html',
                            movies=movies[offset: offset + per_page],
                            page=page,
                            per_page=per_page,
                            pagination=pagination,
                            len=len)

@app.route('/paginate')
def search_results():        
    search_results = [1] * 100
            
    # automatic pagination handling
    total = len(search_results)
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('paginate.html',
                            search_results=search_results[offset: offset + per_page],
                            page=page,
                            per_page=per_page,
                            pagination=pagination,
                            len=len)


######################################################
# 
# Run app
#
######################################################

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True, threaded=True)
