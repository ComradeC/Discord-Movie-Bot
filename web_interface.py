# web_interface.py

# standard modules
import os
import sys

# external modules
from flask import Flask, request, render_template, redirect
from flask_restful import Api, Resource, reqparse
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from dbcon import Movie, Quote
from dotenv import load_dotenv
import psutil


app = Flask(__name__)
app.secret_key = '32346f00914f430b6e53cb3b39ee88c125b89d47a0b938fef5bfd8ba2d4f19ac'
api = Api(app)
load_dotenv()
engine = create_engine('postgresql://' + os.environ['SQL_SECRET'] + '/postgres', echo=True, future=True)


@app.route('/quotes')
def quotes():
    with Session(engine) as session:
        data = session.execute(select(Quote.text, Quote.timestamp, Quote.title))
    return render_template('quotes.html', data=data, cpu_load=psutil.cpu_percent(0.5), memory_load=psutil.virtual_memory()[2])


@app.route('/movies')
def movies():
    with Session(engine) as session:
        data = session.execute(select(Movie.title, Movie.watched_status, Movie.kp_id, Movie.imdb_id))
    return render_template('movies.html', data=data, cpu_load=psutil.cpu_percent(0.5), memory_load=psutil.virtual_memory()[2])


@app.route('/')
def index_page():
    return render_template('index.html')

# dev server launch
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run(host="25.62.170.90")
