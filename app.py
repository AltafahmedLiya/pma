from datetime import datetime
from email.policy import default
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, flash, render_template, url_for, request, redirect,session
from forms import RegistrationForm, LoginForm, PostForm
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from flask_login import LoginManager
import sqlite3
import os
app = Flask(__name__)
app.secret_key=os.urandom(24)

#app.config['SECRET_KEY'] = 'd75dbd5a133d7526b9b3f87469aa475f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

posts = [
    {
        'builder': 'Altaf',
        'property':'Flat',
        'details':'56sqft',
        'date_posted':'April 10 2022'
    },
    {
        'builder': 'Ahmed',
        'property':'plot',
        'details':'100sqft',
        'date_posted':'April 20 2022'
    }
]
@app.route('/',methods=['GET','POST'])
def home():
    return render_template('home.html',posts=posts)

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout', methods=['GET','POST'])
def logout():
    return redirect(url_for('home'))

@app.route('/forgot', methods=['POST','GET'])
def forgot():
        return render_template('/forgot.html')

@app.route('/post/new',methods=['POST','GET'])
def new_post():
        form = PostForm()
        if form.validate_on_submit():
            flash('Your post has been created!','success')
            return redirect(url_for('home'))
        return render_template('/create_post.html', title='New Post', form=form)
        
if __name__ == "__main__":
    app.run(debug=True)