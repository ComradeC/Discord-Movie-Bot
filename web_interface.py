# web_interface.py

# standard modules
import sys

# external modules
from flask import Flask, request, render_template, redirect
from flask_restful import Api, Resource, reqparse
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from dbcon import Movie, Quote

app = Flask(__name__)
api = Api(app)
engine = create_engine('postgresql://Commi:1537@localhost:5432/postgres', echo=True, future=True)


@app.route('/movieDB')
def movies():
    with Session(engine) as session:
        data = session.execute(select(Movie.title, Movie.watched_status))
    return render_template('movies.html', data=data)


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
