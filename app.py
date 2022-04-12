from datetime import datetime
from email.policy import default
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, flash, render_template, url_for, request, redirect,session
from forms import RegistrationForm, LoginForm
import sqlite3
import os
app = Flask(__name__)
app.secret_key=os.urandom(24)

#app.config['SECRET_KEY'] = 'd75dbd5a133d7526b9b3f87469aa475f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


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
@app.route('/')
def home():
    return render_template('home.html',posts=posts)

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

@app.route('/forgot', methods=['POST','GET'])
def forgot():
        return render_template('/forgot.html')

@app.route('/post/new',methods=['POST','GET'])
def new_post():
        return render_template('/create_post.html', title='New Post')
        
if __name__ == "__main__":
    app.run(debug=True)