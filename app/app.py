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
    update_stats()
    return render_template('home.html')

@app.route('/community', methods=['GET', 'POST'])
def community():
    update_stats()
    
    if request.method == 'POST':
        mongo.db.feedbacks.insert_one({
            'user': request.form.get('username'),
            'post': request.form.get('feedback')
        })

    return render_template('community.html', feedbacks=mongo.db.feedbacks.find({}))

@app.route('/contact')
def contact():
    update_stats()
    return render_template('contact.html')
    
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/donate')
def donate():
    return render_template('donate.html')

@app.route('/api/dashboard')
def api_dashboard():
    stats = []

    for entry in mongo.db.stats.find():
        entry['_id'] = str(entry['_id'])
        stats.append(entry)

    return jsonify({'data': stats})

@app.route('/api', methods=['GET', 'POST'])
def api():
    update_stats()
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
    update_stats()
    return render_template('chambers.html')

@app.route('/chamber_1')
def first_chamber():
    update_stats()
    
    movie = mongo.db.movies.find_one({'title': 'The 36th Chamber of Shaolin'})
    return render_template('chamber_1.html', movie=movie)

@app.route('/chamber_2')
def second_chamber():
    update_stats()
    
    movies = mongo.db.movies.find(limit=50)
    return render_template('chamber_2.html', movies=movies)

@app.route('/chamber_3')
def third_chamber():
    update_stats()
    
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
    update_stats()
    
    movies = [movie for movie in mongo.db.movies.find({}, limit=27)]
    return render_template('chamber_4.html', movies=movies[3:])

@app.route('/chamber_5')
def fifth_chamber():
    update_stats()
    movies = [movie for movie in mongo.db.movies.find({}, limit=100)]
    return render_template('chamber_5.html', movies=movies)

@app.route('/chamber_6')
def sixth_chamber():
    update_stats()
    return render_template('chamber_6.html')

@app.route('/chamber_7')
def seventh_chamber():
    #update_stats()
    movies = mongo.db.movies.find(limit=10)
    return render_template('chamber_7.html', movies=movies)

######################################################
# 
# Helper functions
#
######################################################

def update_stats():
    stats = dict(request.headers)
    stats['URL'] = request.url
    stats['Method'] = request.method
    
    if request.headers.getlist("X-Forwarded-For"):
       stats['Ip'] = request.headers.getlist("X-Forwarded-For")[0]
    else:
       stats['Ip'] = request.remote_addr

    #stats['Ip'] = request.remote_addr   #environ.get('HTTP_X_REAL_IP', request.remote_addr)
    stats['Date'] = datetime.datetime.today()
    mongo.db.stats.insert_one(stats)


######################################################
# 
# Run app
#
######################################################

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True, threaded=True)
