import os
import random
import requests
import json

from flask import Flask, render_template

def create_app(test_config = None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'mr.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'hello, World!'
    
    @app.route('/', methods=('GET',))
    def index():
        random.seed()
        imdb_id_rand = 3846190
        response = None

        while(True):
            try:
                imdb_id_rand = '{:0>7}'.format(str(random.randrange(0,9999999)))
                response = requests.get(f'http://www.omdbapi.com/?i=tt{imdb_id_rand}&apikey=bfde1575')
                print(f"Attempting to render movie: {response.json()['Title']}")
            except KeyError as e:
                pass
            else:
                break

        
        return render_template("index.html", movie = response.json())

    
    from . import db
    db.init_app(app)
    
    return app


