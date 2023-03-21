from typing import Pattern
from flask import Flask, redirect, url_for , render_template, request, session, flash 
from flask_sqlalchemy import SQLAlchemy 
from flask_login import UserMixin, login_user, LoginManager, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
from flask_bcrypt import Bcrypt 
from datetime import timedelta
import re

#CONFIG##########################################
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "SomeRandomKey1234"
app.permanent_session_lifetime = timedelta(minutes=5)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db = SQLAlchemy(app)


#USER HANDLER CLASSES ##############################################################
class User(db.Model, UserMixin): 
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), nullable = False, unique = True)
    password = db.Column(db.String(80), nullable = False)

    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password


class RegisterForm(FlaskForm): 
    username = StringField(validators= [InputRequired(), Length(
        min = 4 , max = 20 )], render_kw = {"placeholder": "Enter E-mail here"})
    password = PasswordField (validators = [InputRequired(), Length( 
        min = 4, max = 20)], render_kw = {"placeholder" : "Enter Password"})
    submit = SubmitField("Register")


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = " login " 


@login_manager.user_loader
def load_user(user_id): 
    return User.query.get(int(user_id))

def validate_email(email): 
    pattern = '^[a-z 0-9]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$'
    if re.search(pattern, email): 
        return True
    return False




##############################################################################################################################

@app.route("/logout", methods = ["GET", "POST"])
def logout():
    if "user" in session: 
        logout_user()
        session.pop("user", None)
        #logout_user()
        flash(" You have been logged out")
        return redirect(url_for("home"))
    flash("Not logged in yet!")
    return redirect(url_for("home"))


@app.route("/login", methods = ["GET", "POST"])
def login():
    #If user already logged in
    if "user" in session: 
        return redirect(url_for("contact"))
    #if not! 
    if request.method == "POST": 
        session.permanent = True
        usrname = request.form["nm"]
        password = request.form["psw"]
        #filtering db for first username match
        user = User.query.filter_by(username = usrname).first()

        if user: 
            if bcrypt.check_password_hash(user.password, password): 
                session["user"] = usrname
                login_user(user)
                flash(" You are logged in! ")
                return render_template("contact_me.html")
        flash("Credentials not correct! Try again")
    
    return render_template("login.html")


#Register page if no account possesed 
@app.route("/register", methods = ["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit(): 
        #checking if user exists
        user = User.query.filter_by(username = form.username.data).first()
        if not(user): 
            #checking if email is valid 
            email_valid = validate_email(form.username.data)
            if email_valid: 
                #Hashing psw
                hashed_pwd = bcrypt.generate_password_hash(form.password.data)
                #commiting new user too db
                new_user = User (username = form.username.data, password = hashed_pwd)
                db.session.add(new_user)
                db.session.commit()
                flash(" Congratulation! Your profile has been created...! /n Please login with your new profile! ")
                return redirect(url_for("login"))
            if not email_valid: 
                flash("E-mail invalid")
                return render_template("register.html", form = form )

        flash(" That username already exists. Please choose a different one ")
        return render_template("register.html", form = form )
        
    return render_template("register.html", form = form )




#   PAGES #########################################################################

#Front page / home page 
@app.route("/home")
@app.route("/")
def home():
    return render_template("front_page.html")

#Projects
@app.route("/projects")
def projects():
    return render_template("projects.html")

#About me
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    if "user" in session:

        # en masse kode der understoetter deres kontakt med mig
        return render_template("contact_me.html")

    else : 
        flash(" You need to log in first! ")
        return redirect(url_for("login"))




if __name__ == "__main__": 
    db.create_all()
    app.run(debug=True)


