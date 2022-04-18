from flask import Flask, render_template, url_for , request
import sqlite3
import os
con = sqlite3.connect("PMA")
currentdirectory = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('Login.html')

@app.route("/signupm")
def signupm():
    return render_template('signup.html')

@app.route('/signup', methods =["GET", "POST"])
def signup():
    Fname = request.form.get("Fname")
    Lname = request.form.get("Lname")
    password = request.form.get("password")
    Cpassword = request.form.get("confirmPassword") 
    print(Fname)
    print(Lname)
    print(password)
    print(Cpassword)
    #query1 = "INSERT INTO signup (Fname, Lname, password,Cpassword) VALUES('{fn}','{ln}','{pws}','{cpws}')".format(fn = Fname,ln = Lname,pws = password,cpws = Cpassword)
    query1 = "insert into signup(Fname, Lname, Password, Cpassword) values('"+Fname+"','"+Lname+"','"+password+"','"+Cpassword+"')"
    con.execute(query1)
    con.commit()
    con.close()
    return render_template('signup.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

if __name__=="__main__":
    app.run(debug=True)