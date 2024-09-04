from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()


app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_key')
app.config['MOVIE_DB_API_KEY'] = os.getenv('MOVIE_DB_API_KEY')
app.config['TV_DB_API_KEY'] = os.getenv('TV_DB_API_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
Bootstrap5(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


MOVIE_DB_SEARCH_URL = os.getenv('MOVIE_DB_SEARCH_URL')
MOVIE_DB_INFO_URL = os.getenv('MOVIE_DB_INFO_URL')
MOVIE_DB_IMAGE_URL = os.getenv('MOVIE_DB_IMAGE_URL')

TV_DB_SEARCH_URL = os.getenv('TV_DB_SEARCH_URL')
TV_DB_INFO_URL = os.getenv('TV_DB_INFO_URL')
TV_DB_IMAGE_URL = os.getenv('TV_DB_IMAGE_URL')


#TABLES
class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.email}>"


class Movie(db.Model):
   id: Mapped[int] = mapped_column(Integer, primary_key=True)
   title: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
   year: Mapped[int] = mapped_column(Integer, nullable=False)
   description: Mapped[str] = mapped_column(String(500), nullable=False)
   rating: Mapped[float] = mapped_column(Float, nullable=True)
   ranking: Mapped[int] = mapped_column(Integer,nullable=True)
   review: Mapped[str] = mapped_column(String(250),nullable=True)
   img_url: Mapped[str] = mapped_column(String(250), nullable=False)


class TVShow(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
   
with app.app_context():
    db.create_all()

    
#FORMS
class RateMovieForm(FlaskForm):
   rating = StringField("Update Rating Out of 10 e.g. 5.5", validators=[DataRequired()])
   review = StringField("Update Review", validators=[DataRequired()])
   submit = SubmitField("Done")

class AddMovie(FlaskForm):
   title = StringField("Movie Title", validators=[DataRequired()])
   submit = SubmitField("Search")

class RateTVShowForm(FlaskForm):
    rating = StringField("Update Rating Out of 10 e.g. 5.5", validators=[DataRequired()])
    review = StringField("Update Review", validators=[DataRequired()])
    submit = SubmitField("Done")

class AddTVShowForm(FlaskForm):
    title = StringField("TV Show Title", validators=[DataRequired()])
    submit = SubmitField("Search")


#ROUTES
@app.route("/")
def home():

    movie_result = db.session.execute(db.select(Movie).order_by(Movie.rating))
    all_movies = movie_result.scalars().all()

    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()

    tv_show_result = db.session.execute(db.select(TVShow).order_by(TVShow.rating))
    all_tv_shows = tv_show_result.scalars().all()

    for i in range(len(all_tv_shows)):
        all_tv_shows[i].ranking = len(all_tv_shows) - i
    db.session.commit()

    return render_template("index.html", movies=all_movies, tv_shows=all_tv_shows)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        errors = []

        if len(password) < 8:
            errors.append('Password must be at least 8 characters long.')

        if password != confirm_password:
            errors.append('Passwords do not match.')

        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            errors.append('Email already exists.')

        if errors:
            return redirect(url_for('signup', errors=errors))

        hashed_password = generate_password_hash(password)
        new_user = User(first_name=first_name, last_name=last_name, email=email, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Sign-up successful! Please log in.','success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating your account.', 'danger')
            return redirect(url_for('signup'))

    return render_template('signup.html')


@app.route('/add_movie_redirect')
def add_movie_redirect():
    if not current_user.is_authenticated:
        flash('You must be logged in to add Movie.', 'warning')
        return redirect(url_for('login', next=url_for('add_movie')))
    return redirect(url_for('add_movie'))

@app.route('/add_tv_show_redirect')
def add_tv_show_redirect():
    if not current_user.is_authenticated:
        flash('You must be logged in to Tv Show.', 'warning')
        return redirect(url_for('login', next=url_for('add_tv_show')))
    return redirect(url_for('add_tv_show'))



@app.route('/add', methods=["GET", "POST"])
@login_required
def add_movie():
    form = AddMovie()
    movies = []
    searched = False

    if form.validate_on_submit():
        movie_title = form.title.data
        api_key = app.config['MOVIE_DB_API_KEY']
        response = requests.get(MOVIE_DB_SEARCH_URL, params={"api_key": api_key, "query": movie_title})
        data = response.json().get('results', [])

        for item in data:
            movie = {
                "id": item['id'],
                "title": item['title'],
                "release_date": item['release_date'],
                "img_url": f"{MOVIE_DB_IMAGE_URL}{item['poster_path']}"
            }
            movies.append(movie)
        searched = True

    return render_template("add_movie.html", form=form, movies=movies, searched=searched)



@app.route('/add_tv_show', methods=["GET", "POST"])
@login_required
def add_tv_show():
    form = AddTVShowForm()
    tv_shows = []
    searched = False

    if form.validate_on_submit():
        searched = True 
        tv_show_title = form.title.data
        api_key = app.config['TV_DB_API_KEY']
        response = requests.get(TV_DB_SEARCH_URL, params={"api_key": api_key, "query": tv_show_title})
        data = response.json().get('results', [])

        for item in data:
            tv_show = {
                "id": item['id'],
                "name": item['name'], 
                "first_air_date": item.get('first_air_date', 'N/A'),
                "img_url": f"{TV_DB_IMAGE_URL}{item['poster_path']}"
            }
            tv_shows.append(tv_show)

    return render_template("add_tvshow.html", form=form, tv_shows=tv_shows, searched=searched)


 
@app.route("/edit", methods=["GET", "POST"])
@login_required
def rate_movie():
   form = RateMovieForm()
   movie_id = request.args.get('id')
   movie  = db.get_or_404(Movie, movie_id)
   if form.validate_on_submit():
      movie.rating = float(form.rating.data)
      movie.review = form.review.data
      db.session.commit()
      flash('Movie added!', 'success')
      return redirect(url_for('home'))
   return render_template('update_movie.html', movie=movie, form=form)


@app.route("/edit_tv_show", methods=["GET", "POST"])
@login_required
def rate_tv_show():
    form = RateTVShowForm()
    tv_show_id = request.args.get('id')
    tv_show = db.get_or_404(TVShow, tv_show_id)
    if form.validate_on_submit():
        tv_show.rating = float(form.rating.data)
        tv_show.review = form.review.data
        db.session.commit()
        flash('Tv Show added!', 'success')
        return redirect(url_for('home'))
    return render_template('update_tvshow.html', tv_show=tv_show, form=form)



@app.route('/delete')
@login_required
def delete_movie():
   movie_id = request.args.get('id')
   movie  = db.get_or_404(Movie, movie_id)
   db.session.delete(movie)
   db.session.commit()
   return redirect(url_for('home'))


@app.route('/delete_tv_show')
@login_required
def delete_tv_show():
    tv_show_id = request.args.get('id')
    tv_show = db.get_or_404(TVShow, tv_show_id)
    db.session.delete(tv_show)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/find')
def find_movie():
   movie_api_id = request.args.get('id')
   if movie_api_id:
      movie_api_url = f"{MOVIE_DB_INFO_URL}/{movie_api_id}"
      api_key = app.config['MOVIE_DB_API_KEY']
      response = requests.get(movie_api_url, params={"api_key": api_key, "language": "en-US"})
      data = response.json()
      new_movie = Movie(
         title=data['title'],
         year=data["release_date"].split("-")[0],
         img_url=f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}",
         description=data["overview"]
      )
      db.session.add(new_movie)
      db.session.commit()
      return redirect(url_for("rate_movie", id=new_movie.id))


@app.route('/find_tv_show')
def find_tv_show():
    tv_show_api_id = request.args.get('id')
    if tv_show_api_id:
        tv_show_api_url = f"{TV_DB_INFO_URL}/{tv_show_api_id}"
        api_key = app.config['TV_DB_API_KEY']
        response = requests.get(tv_show_api_url, params={"api_key": api_key, "language": "en-US"})
        data = response.json()
        new_tv_show = TVShow(
            title=data['name'],
            year=data["first_air_date"].split("-")[0],
            img_url=f"{TV_DB_IMAGE_URL}{data['poster_path']}",
            description=data["overview"]
        )
        db.session.add(new_tv_show)
        db.session.commit()
        return redirect(url_for("rate_tv_show", id=new_tv_show.id))
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
