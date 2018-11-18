from flask import Flask, render_template, Markup, request, url_for, redirect, flash, session, logging, g
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from data import info
import sqlite3

MyApp = Flask(__name__)
MyApp.secret_key = 'leroybiggins'
info = info()


MyApp.debug = True

@MyApp.route('/login')
def login():
  return render_template('login.html')
  
@MyApp.route('/')
def home():
  return render_template('index.html')
  
@MyApp.route('/about')
def about():
  return render_template('about.html')
  
@MyApp.route('/info')
@MyApp.route('/info/<dog>/')
def dogInfo(dog=None):
  return render_template('info.html', dog=dog) 
  
@MyApp.route('/gallery')
def pics():  
  return render_template('gallery.html', info = info)
  

class RegisterForm(Form):
  username = StringField('Username',[validators.Length(min=1,max=100)])
  email = StringField('Email',[validators.Length(min=5,max=100)])
  password = PasswordField('Password',[validators.DataRequired(),validators.EqualTo('confirm',message='Passwords do not match')])
  confirm = PasswordField('Confirm Password')    

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
      return render_template('register.html',form=form)
    except:
      con.close()
      flash('That username is already taken','error')
  return render_template('register.html',form=form)

              
if __name__ == "__main__":
  MyApp.run()
 
