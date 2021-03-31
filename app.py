import os
from flask import (
    Flask, flash, render_template, 
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__) # create instance of Flask in a variable called "app"

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


@app.route("/") # the forward slash "/" refers to the default route
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/") 
@app.route("/get_movies")
def get_movies():
    # This will sort the movie list alphabetically in list page
    movies = list(mongo.db.movies.find().sort("movie_name", 1))
    return render_template("movies.html", movies=movies)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    movies = list(mongo.db.movies.find({"$text": {"$search": query}}))
    return render_template("movies.html", movies=movies)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user: # this is "truly", ie if "existing_user == true"
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
            # if you want the user to re-confirm password, add a line here 
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful")
        return redirect(url_for("profile", username=session["user"])) # this will redirect the user to the profile page
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            #ensure hashed password matches user input
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


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    #grab the session user's username from the db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)
        # we need to pass the "username" variable here

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


# adding this myself
@app.route("/movie_page/<movie_name>")
def movie_page(movie_name):
    # page redirect to the particular movie on click from movie list page
    get_movie = mongo.db.movies.find_one({"movie_name": movie_name})
    reviews = list(mongo.db.reviews.find({"movie_name": movie_name}))
    return render_template("movie_page.html", 
        get_movie=get_movie, reviews=reviews)


@app.route("/add_movie", methods=["GET", "POST"])
def add_movie():
    if request.method == "POST":
        #Check if movie exists
        #add this myself, unable to make it work without case sensitivity
        existing_movie = mongo.db.movies.find_one(
            {"movie_name": request.form.get("movie_name")})

        if existing_movie:
            #add this myself
            flash("Movie already exists")
            return redirect(url_for("add_movie"))

        movie = {
            "movie_name": request.form.get("movie_name"),
            "year": request.form.get("year"),
            "genre": request.form.get("genre"),
            #if genre was a checkbox selection, 
            #will need to use "request.form.getlist('genre')"
            "director": request.form.get("director"),
            "cast": request.form.get("cast"),
            "image": request.form.get("image")
        }
        mongo.db.movies.insert_one(movie) #here we insert the variable "movie" into insert_one()
        flash("Movie Successfully Added")
        return redirect(url_for("movie_page", movie_name=request.form.get("movie_name"))) 
        # IMPORTANT WORK IN PROGRESS - Here will need to add the REVIEWS database and link it with the MOVIES database
    return render_template("add_movie.html")


@app.route("/edit_movie/<movie_id>", methods=["GET", "POST"])
def edit_movie(movie_id):
    if request.method == "POST":
        submit = {
            "movie_name": request.form.get("movie_name"),
            "year": request.form.get("year"),
            "genre": request.form.get("genre"),
            #if genre was a checkbox selection, 
            #will need to use "request.form.getlist('genre')"
            "director": request.form.get("director"),
            "cast": request.form.get("cast"),
            "image": request.form.get("image")
        }
        mongo.db.movies.update({"_id": ObjectId(movie_id)}, submit)
        # update method takes 2 parameters, both of which are dictionaries. 
        # This line here searches for the movie in the database by the movie_id, 
        # once found it will update the movie with the "submit" dictionary which contains all the form elements 
        flash("Movie Successfully Edited")

    # the "_id" is whats on mongodb and in a bson data type(string of letters and nums)
    movie = mongo.db.movies.find_one({"_id": ObjectId(movie_id)})
    return render_template("edit_movie.html", movie=movie) #Not sure how to redirect back to "movie_page.html" for specific movie


@app.route("/movie_page/delete_movie/<movie_id>")
def delete_movie(movie_id):
    mongo.db.movies.remove({"_id": ObjectId(movie_id)})
    flash("Movie Successfully Removed")
    return redirect(url_for("get_movies"))


#adding review function not working!!!
@app.route("/movie_page/<movie_name>", methods=["POST"])
def add_review(movie_name):
    print("IN THE METHOD")
    if request.method == "POST":
        print("IN THE POST PART")
        review = {
            "movie_name": movie_name,
            "review_description": request.form.get("review_description"),
            "by_user": session["user"]
        }
        mongo.db.reviews.insert_one(review)

    flash("Your review was added")
    return redirect(url_for("movie_page", movie_name=movie_name))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True) # IMPORTANT - Make sure to change to 
                        #"debug=False" prior to actual deployment
