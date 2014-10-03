"""
Copyright (C) 2014, Jill Huchital
"""

# test comment

from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request

from playlists import get_all_playlists

app = Flask(__name__)

@app.route('/')
def index():
    # return render_template('index.html', greeting='here we are then')
    return "index"

@app.route('/hello/')
def hello():
    return render_template('index.html')

@app.route('/api/1.0/get_playlists', methods = ['POST'])
def get_playlists():
    retval = get_all_playlists()
    return jsonify({'all_playlists': retval})

if __name__ == '__main__':
    app.run(debug = True)
