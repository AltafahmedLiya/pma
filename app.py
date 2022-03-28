from flask import Flask, flash, render_template, url_for, request, redirect,session
import sqlite3
import os

app = Flask(__name__)
app.secret_key=os.urandom(24)

conn = sqlite3.connect('dpma', check_same_thread=False)
cursor=conn.cursor()
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect('/')

@app.route('/login_validation', methods=['POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')
    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email,password))
    users = cursor.fetchall()
    if len(users)>0:
        session['user_id']=users[0][0]
        flash(f'Login Successful')
        return redirect('/home')
    else:
        flash(f'Login Failed')
        return redirect('/')

@app.route('/registeration',methods=['POST'])
def registeration():
        name=request.form.get('rname')
        email=request.form.get('remail')
        password=request.form.get('rpassword')
        cursor.execute("""INSERT INTO `users` (`user_id`,`name`,`email`,`password`) VALUES(NULL,'{}','{}','{}')""".format(name,email,password))
        conn.commit()
        return "User Registered successfully"

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

@app.route('/forgot', methods=['POST','GET'])
def forgot():
        return render_template('/forgot.html')

if __name__ == "__main__":
    app.run(debug=True)