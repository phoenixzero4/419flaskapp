from flask import Flask, render_template, Markup, request, url_for, redirect, flash, session, logging, g, abort
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from data import info
import sqlite3

MyApp = Flask(__name__)
MyApp.secret_key = 'leroybiggins'
MyApp.debug = True
info = info()

class RegisterForm(Form):
  username = StringField('Username',[validators.Length(min=1,max=100)])
  email = StringField('Email',[validators.Length(min=5,max=100)])
  password = PasswordField('Password',[validators.DataRequired(),validators.EqualTo('confirm',message='Passwords do not match')])
  confirm = PasswordField('Confirm Password')   

class LoginForm(Form):
  username = StringField('Username')
  password = PasswordField('Password')

@MyApp.route('/')
def home():
  return render_template('index.html')
  
@MyApp.route('/about')
def about():
  return render_template('about.html')
  
@MyApp.route('/info')
@MyApp.route('/info/<dog>/')
def dogInfo(dog=None):
  id=0
  for n in info:
    if dog == n['name']:
      id = n['id']
    var = info[id-1]
  return render_template('info.html', dogname=dog, info=info, var=var) 
  
@MyApp.route('/gallery')
def pics():  
  return render_template('gallery.html', info = info)

@MyApp.route('/register', methods= ['GET','POST'])
def register():
  import sqlite3
  form = RegisterForm(request.form)
  if request.method == 'POST' and form.validate():
    username = form.username.data
    email = form.email.data
    password = str(form.password.data)
  
    con = sqlite3.connect('test.db')
    cur = con.cursor()
    try:
      cur.execute("INSERT INTO users VALUES (?,?,?)",(username,email,password))
      con.commit()
      con.close()
      flash('Your account has been registered. You can now login','success')
      redirect(url_for('login'))
      return render_template('login.html',form=form)
    except:
      con.close()
      flash('That username is already taken','error')
  return render_template('register.html',form=form)

@MyApp.route('/login', methods=['GET','POST'])
def login():
  form = LoginForm(request.form)

  if request.method == 'POST':
    user = request.form['username']
    password_maybe = request.form['password']
    password = None
    con = sqlite3.connect('test.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    result = cur.execute("SELECT * FROM users WHERE username = '"+ user+"'")
    
    for row in result:
      session['id'] = row['email'] + row['username']
      session['username'] = row['username']
      password = row['password']
    con.close()
    if password_maybe == password:
      return render_template('index.html',form=form)
    else:
      flash('Incorrect username or password','error')
      return render_template('login.html',form=form)
  return render_template('login.html',form=form)   

@MyApp.route('/logout')
def logout():
  if 'username' in session:
    session.pop('id',None)
    flash('You have successfully logged out of your account','success')
    return render_template('index.html')
  return 'This shouldn\'t happen. \nYou are not logged in'


  
if __name__ == "__main__":
  MyApp.run()
 
