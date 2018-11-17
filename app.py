from flask import Flask, render_template, Markup, request, url_for
from data import info
import random

MyApp = Flask(__name__)

info = info()
#url_for('style',filename='primary.css')

@MyApp.route('/login')
def login():
  return '<h1>Future login page</h1>'
  
@MyApp.route('/register')
def register():
  return '<h1>Future registration page</h1>'
  
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
  


              
if __name__ == "__main__":
        MyApp.run()
 
