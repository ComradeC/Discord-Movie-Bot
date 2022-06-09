# web_interface.py

# standard modules
import sys

# external modules
from flask import Flask, request, render_template, redirect
from flask_restful import Api, Resource, reqparse
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from dbcon import Movie, Quote
import psutil

app = Flask(__name__)
app.secret_key = '32346f00914f430b6e53cb3b39ee88c125b89d47a0b938fef5bfd8ba2d4f19ac'
api = Api(app)
engine = create_engine('postgresql://Commi:1537@localhost:5432/postgres', echo=True, future=True)


@app.route('/movieDB')
def movies():
    with Session(engine) as session:
        data = session.execute(select(Movie.title, Movie.watched_status, Movie.kp_id, Movie.imdb_id))
    return render_template('movies.html', data=data, cpu_load=psutil.cpu_percent(0.5), memory_load=psutil.virtual_memory()[2])


@app.route('/quoteDB')
def quotes():
    with Session(engine) as session:
        data = session.execute(select(Quote))
    return render_template('quotes.html', data=data)


@app.route('/')
def main():
    return redirect('movieDB')


# server launch
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run(host="25.62.170.90")
