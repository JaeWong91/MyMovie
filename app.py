import os
import math
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
# from https://www.codegrepper.com/code-examples/python/datetime+today
if os.path.exists("env.py"):
    import env


app = Flask(__name__)  # create instance of Flask in a variable called "app"

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


@app.route("/")  # the forward slash "/" refers to the default route
@app.route("/home")
def home():
    return render_template("home.html")


# movie list
@app.route("/")
@app.route('/get_movies')
def get_movies():
    """Logic for movie list and pagination"""
    # number of movies per page
    per_page = 6
    page = int(request.args.get('page', 1))
    # count total number of movies
    total = mongo.db.movies.count_documents({})
    # logic for what movies to return
    movies = mongo.db.movies.find().sort(
        "movie_name", 1).skip((page - 1)*per_page).limit(per_page)
    pages = range(1, int(math.ceil(total / per_page)) + 1)
    return render_template(
        'movies.html', movies=movies, page=page, pages=pages, total=total)


# search query
@app.route("/get_movies/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    movies = list(mongo.db.movies.find({"$text": {"$search": query}}))
    return render_template("movies.html", movies=movies)


# register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful")
        # this will redirect the user to the profile page
        return redirect(url_for("profile", username=session["user"]))
    return render_template("register.html")


# login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome, {}".format(
                        request.form.get("username")))
                    return redirect(url_for(
                        "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))
        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))
    return render_template("login.html")


# profile
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from the db
    reviews = mongo.db.reviews.find().sort("review_date", -1)
    movies = mongo.db.movies.find()
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template(
            "profile.html", username=username,
            reviews=reviews, movies=movies)
    return redirect(url_for("login"))


# Log Out
@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("You have been logged out")
    session.clear()
    return redirect(url_for("login"))


# Movie Page
@app.route("/movie_page/<movie_id>")
def movie_page(movie_id):
    # page redirect to the particular movie on click from movie list page
    # obtain specific movie and list of all reviews for that movie
    get_movie = mongo.db.movies.find_one({"_id": ObjectId(movie_id)})
    reviews = list(mongo.db.reviews.find(
        {"movie_id": ObjectId(movie_id)}).sort("review_date", -1))
    already_reviewed = False

    # determine if a user is logged in
    user = ""
    try:
        user = session["user"]
    except KeyError:
        user = None

    # This is to limit 1 review per user
    if user:
        for review in reviews:
            if review["by_user"] == session["user"]:
                already_reviewed = True

    return render_template(
        "movie_page.html",
        get_movie=get_movie,
        reviews=reviews, already_reviewed=already_reviewed)


# Add Movie
@app.route("/add_movie", methods=["GET", "POST"])
def add_movie():
    if session:
        if session['user'] == "admin":
            if request.method == "POST":
                # Check if movie exists
                existing_movie = mongo.db.movies.find_one(
                    {"movie_name": request.form.get("movie_name")})

                if existing_movie:
                    flash("Movie already exists")
                    return redirect(url_for("add_movie"))

                movie = {
                    "movie_name": request.form.get("movie_name"),
                    "year": request.form.get("year"),
                    "genre": request.form.get("genre"),
                    "director": request.form.get("director"),
                    "cast": request.form.get("cast"),
                    "image": request.form.get("image")
                }
                mongo.db.movies.insert_one(movie)
                flash("Movie Successfully Added")
                return redirect(url_for("get_movies"))
            return render_template("add_movie.html")
        return render_template("403.html")
    return render_template("403.html")


# edit movie
@app.route("/edit_movie/<movie_id>", methods=["GET", "POST"])
def edit_movie(movie_id):
    if request.method == "POST":
        submit = {
            "movie_name": request.form.get("movie_name"),
            "year": request.form.get("year"),
            "genre": request.form.get("genre"),
            "director": request.form.get("director"),
            "cast": request.form.get("cast"),
            "image": request.form.get("image")
        }
        mongo.db.movies.update({"_id": ObjectId(movie_id)}, submit)

        flash("Movie Successfully Edited")
        return redirect(url_for("movie_page", movie_id=movie_id))

    movie = mongo.db.movies.find_one({"_id": ObjectId(movie_id)})
    return render_template("edit_movie.html", movie=movie)


# Delete Movie
@app.route("/movie_page/delete_movie/<movie_id>")
def delete_movie(movie_id):
    mongo.db.movies.remove({"_id": ObjectId(movie_id)})
    flash("Movie Successfully Removed")
    return redirect(url_for("get_movies"))


# Add Review
@app.route("/movie_page/<movie_id>", methods=["POST"])
def add_review(movie_id):
    if request.method == "POST":
        now = datetime.now()
        review = {
            "movie_id": ObjectId(movie_id),
            "movie_name": request.form.get("movie_name"),
            "review_rating": request.form.get("review_rating"),
            "review_description": request.form.get("review_description"),
            "by_user": session["user"],
            "review_date": now.strftime("%d-%m-%Y %H:%M")
        }
        mongo.db.reviews.insert_one(review)

    flash("Your review was added")
    return redirect(url_for("movie_page", movie_id=movie_id))


# Edit Review
@app.route("/edit_review/<review_id>", methods=["GET", "POST"])
def edit_review(review_id):
    movie_id = request.form.get("movie_id")
    if request.method == "POST":
        now = datetime.now()
        submit = {
            "movie_id": ObjectId(movie_id),
            "movie_name": request.form.get("movie_name"),
            "review_rating": request.form.get("review_rating"),
            "review_description": request.form.get("review_description"),
            "by_user": request.form.get("by_user"),
            "review_date": request.form.get("review_date"),
            "edit_date": now.strftime("%d-%m-%Y %H:%M")
        }
        mongo.db.reviews.update({"_id": ObjectId(review_id)}, submit)
        return redirect(url_for("movie_page", movie_id=movie_id))

    review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
    return render_template("edit_review.html", review=review)


# Delete Review
@app.route("/delete_review/<review_id>")
def delete_review(review_id):
    mongo.db.reviews.remove({"_id": ObjectId(review_id)})
    flash("Review Successfuly Removed")
    return redirect(request.referrer)
    # This line taken from https://stackoverflow.com/questions
    # /41270855/flask-redirect-to-same-page-after-form-submission


# Delete Review from Profile
@app.route("/delete_review_profile/<review_id>")
def delete_review_profile(review_id):
    mongo.db.reviews.remove({"_id": ObjectId(review_id)})
    flash("Review Successfuly Removed")
    return redirect(url_for("profile", username=session["user"]))


# custom 404 page
@app.errorhandler(404)
def error_404(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


# custom 403 page - forbidden page
@app.errorhandler(403)
def error_403(e):
    # note that we set the 403 status explicitly
    return render_template('403.html'), 403


# custom 500 page - internal server error
@app.errorhandler(500)
def error_500(e):
    # note that we set the 500 status explicitly
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)  # IMPORTANT - Make sure to change to
# "debug=False" prior to actual deployment
