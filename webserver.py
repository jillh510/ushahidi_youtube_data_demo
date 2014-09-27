"""
Copyright (C) 2014, Jill Huchital
"""

# test comment

from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request

from playlists import get_all_playlists, create_playlists, get_all_categories, add_new_category, add_new_topic, get_all_topics
from db import connect_to_db

ALL_DBS = None

app = Flask(__name__)

@app.route('/')
def index():
    # return render_template('index.html', greeting='here we are then')
    return "index"

@app.route('/hello/')
def hello():
    return render_template('index.html', greeting='here we are')

@app.route('/tools/')
def tools():
    return render_template('tools.html')

@app.route('/api/1.0/create_playlists', methods = ['POST'])
def do_create_playlists():
    create_playlists(ALL_DBS)
    retval = get_all_playlists(ALL_DBS)
    return jsonify({'all_playlists': retval})

@app.route('/api/1.0/get_playlists', methods = ['POST'])
def get_playlists():
    retval = get_all_playlists(ALL_DBS)
    return jsonify({'all_playlists': retval})

@app.route('/api/1.0/get_all_categories', methods = ['POST'])
def get_categories():
    retval = get_all_categories(ALL_DBS)
    return jsonify({'all_categories': retval})

@app.route('/api/1.0/get_all_topics', methods = ['POST'])
def get_topics():
    retval = get_all_topics(ALL_DBS)
    return jsonify({'all_topics': retval})

@app.route('/api/1.0/add_category', methods = ['POST'])
def add_category():
    retval = add_new_category(request.json, ALL_DBS)
    return retval

@app.route('/api/1.0/add_topic', methods = ['POST'])
def add_topic():
    retval = add_new_topic(request.json, ALL_DBS)
    return jsonify({'return_code': retval})

@app.route('/api/1.0/<string:api_call>', methods = ['POST'])
def generic_api_call(api_call):
    if not request.json:
        abort(400)
    param1 = request.json.get('param1', 'no param 1')
    param2 = request.json.get('param2', 'no param 2')
    retval = {'param_1': param1,
            'api_call': api_call,
            'param_2': param2}
    return jsonify(retval)

if __name__ == '__main__':
    # debug = True makes the server restart when the Python files change. TODO: make it
    # depend on whether we're running locally or in production.
    ALL_DBS = connect_to_db()
    # create_playlists(ALL_DBS)
    app.run(debug = True)
