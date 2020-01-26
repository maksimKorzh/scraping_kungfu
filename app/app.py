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
from flask import jsonify
from flask import Response
from flask_pymongo import PyMongo
from flask_paginate import Pagination, get_page_args
import json
import datetime


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

@app.route('/community', methods=['GET', 'POST'])
def community():
    if request.method == 'POST':
        mongo.db.feedbacks.insert_one({
            'user': request.form.get('username'),
            'post': request.form.get('feedback'),
            'date': request.form.get('date')
        })

    return render_template('community.html', feedbacks=mongo.db.feedbacks.find({}))

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/api', methods=['GET', 'POST'])
def api():
    response = []
    
    for movie in mongo.db.movies.find({}):
        movie['_id'] = str(movie['_id'])
        response.append(movie)
    
    if request.method == 'POST':
        index = int(request.args.get('index'))
        limit = int(request.args.get('limit'))
        
        return jsonify({'data': response[index:index+limit]})
    else:
        return jsonify({'data': response})

@app.route('/chambers')
def about():
    return render_template('chambers.html')

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

@app.route('/chamber_4')
def fourth_chamber():
    movies = [movie for movie in mongo.db.movies.find({}, limit=27)]
    return render_template('chamber_4.html', movies=movies[3:])

@app.route('/chamber_5')
def fifth_chamber():
    movies = [movie for movie in mongo.db.movies.find({}, limit=100)]
    return render_template('chamber_5.html', movies=movies)

@app.route('/chamber_6')
def sixth_chamber():
    return render_template('chamber_6.html')

@app.route('/chamber_7')
def seventh_chamber():
    movies = mongo.db.movies.find(limit=10)
    return render_template('chamber_7.html', movies=movies)


######################################################
# 
# Run app
#
######################################################

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True, threaded=True)
