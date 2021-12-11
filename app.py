from enum import unique
from logging import NullHandler
from os import urandom
import random
from flask import Flask , render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from werkzeug.utils import redirect
#from sqlalchemy.ext.declarative.api import declarative_base

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
global j,i
j,i=0,1

class Todo(db.Model):
    sno = db.Column(db.Integer ,primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route('/',methods=['GET','POST'])

def hello_world():
    n=random.random()
    n=n*100000000000
    n=int(n)
    if request.method=="POST":
        title =(request.form['title'])
        desc =(request.form['desc'])
        todo = Todo(sno=n,title=title,desc=desc)
   
        db.session.add(todo)
    
        db.session.commit()
    
    
    allTodo =Todo.query.all()
    
    return render_template('index.html',allTodo=allTodo)
    
    
    #return 'Hello, World!'
@app.route('/show')
def products():
    allTodo =Todo.query.all()
    
    
    return 'This is sahil!'
@app.route('/update/<int:sno>',methods =['GET','POST'])
def update(sno):
    if request.method=="POST":
        title =(request.form['title'])
        desc =(request.form['desc'])
        todo =Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
    
        db.session.commit()
        return redirect("/")
        

    todo =Todo.query.filter_by(sno=sno).first()
    
    
    return render_template('update.html',todo=todo)
@app.route('/delete/<int:sno>')
def delete(sno):
    todo =Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    
    return redirect("/")
    
if __name__ == '__main__':
    app.run(debug=True,port =8000)
