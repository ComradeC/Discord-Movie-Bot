# web_interface.py

# standard modules
import sys

# external modules
import flask_login
from flask import Flask, request, render_template, redirect, flash
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import select, delete, update
from sqlalchemy.sql.expression import func
from flask_login import LoginManager, login_required
from flask_wtf import CSRFProtect
import psutil

# local modules
from models import UserModel, MovieModel, QuoteModel, DowQuoteModel
from settings import FLASK_APP_SECRET, Session
from id_lookup import kp_id_lookup, imdb_id_lookup

app = Flask(__name__)
app.secret_key = FLASK_APP_SECRET

login_manager = LoginManager()
login_manager.init_app(app)

csrf = CSRFProtect()
csrf.init_app(app)


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    with Session() as db_session:
        if username not in db_session.scalars(select(UserModel.username)):
            return

    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(r):
    username = r.form.get('username')
    with Session() as db_session:
        if username not in db_session.scalars(select(UserModel.username)):
            return

    user = User()
    user.id = username
    return user


@app.route('/quotes')
def quotes():
    with Session() as db_session:
        data = db_session.scalars(select(QuoteModel))
        dow_quote = db_session.execute(select(DowQuoteModel.text).order_by(func.random())).fetchone()
        return render_template('quotes.html', data=data, dow_quote=dow_quote[0])


@app.route('/movies')
def movies():
    with Session() as db_session:
        data = db_session.scalars(select(MovieModel).order_by(MovieModel.id))
        return render_template('movies.html', data=data)


@app.route('/')
def index_page():
    return redirect('/movies')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        username = request.form['username']
        error = None

        with Session() as db_session:
            if username is None:
                error = 'Enter username.'

            elif check_password_hash(db_session.scalar(select(UserModel.password).where(UserModel.username == username)), request.form['password']) is False:
                error = 'Incorrect username/password.'

        if error is None:
            user = User()
            user.id = username
            flask_login.login_user(user)
            return redirect('/movies')

        return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect('/movies')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        return render_template('signup.html')
    elif request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        repeat_password = request.form['repeat_password']
        error = None

        if username is None:
            error = 'Username is required.'
        elif password is None:
            error = 'Password is required.'
        elif repeat_password is None:
            error = 'Please repeat password.'
        elif repeat_password != password:
            error = "Passwords don't match"

        if error is None:

            try:
                with Session() as db_session:
                    user = UserModel(username=username, password=generate_password_hash(password))
                    db_session.add(user)
                    db_session.commit()

            except db_session.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect('/login')

        flash(error)


@app.route('/movies/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete_movie(movie_id):
    with Session() as db_session:
        db_session.execute(delete(MovieModel).where(MovieModel.id == movie_id))
        db_session.commit()
    return redirect('/movies')


@app.route('/movies/update/<int:movie_id>', methods=['POST'])
@login_required
def update_movie(movie_id):
    with Session() as db_session:
        title = request.form['title']
        if request.form.get('watched_status'):
            watched_status = True
        else:
            watched_status = False
        kp_id = request.form['kp_id']
        imdb_id = request.form['imdb_id']

        db_session.execute(update(MovieModel)
                           .where(MovieModel.id == movie_id)
                           .values(title=title, watched_status=watched_status, kp_id=kp_id, imdb_id=imdb_id))
        db_session.commit()
    return redirect('/movies')


@app.route('/quotes/delete/<int:quote_id>', methods=['POST'])
@login_required
def delete_quote(quote_id):
    with Session() as db_session:
        db_session.execute(delete(QuoteModel).where(QuoteModel.id == quote_id))
        db_session.commit()
    return redirect('/quotes')


@app.route('/quotes/update/<int:quote_id>', methods=['POST'])
@login_required
def update_quote(quote_id):
    with Session() as db_session:
        text = request.form['text']
        title = request.form['title']
        timestamp = request.form['timestamp']

        db_session.execute(update(QuoteModel)
                           .where(QuoteModel.id == quote_id)
                           .values(text=text, title=title, timestamp=timestamp))
        db_session.commit()
    return redirect('/quotes')


@app.route('/movies/new', methods=['POST'])
@login_required
def new_movie():
    with Session() as db_session:
        title = request.form['title']
        kp_id = kp_id_lookup(title)
        imdb_id = imdb_id_lookup(title)
        movie = MovieModel(title=title, watched_status=False, kp_id=kp_id, imdb_id=imdb_id)

        db_session.add(movie)
        db_session.commit()
    return redirect('/movies')


@app.route('/quotes/new', methods=['POST'])
@login_required
def new_quote():
    with Session() as db_session:
        text = request.form['text']
        title = request.form['title']
        timestamp = request.form['timestamp']
        quote = QuoteModel(text=text, title=title, timestamp=timestamp)

        db_session.add(quote)
        db_session.commit()
    return redirect('/quotes')


@app.route('/performance')
@login_required
def performance():
    perf_data = {'cpu_load': psutil.cpu_percent(0.5), 'memory_load': psutil.virtual_memory()[2]}
    return render_template('perf_mon.html', perf_data=perf_data)


# dev server launch
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run(host="0.0.0.0", port=5000)
