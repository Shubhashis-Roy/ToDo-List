# Minimal Application
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
# from flask import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"  #/ ToDO:- Replace sql lite with mongodb database   
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
db=SQLAlchemy(app)

class Todo(db.Model):
    #Write all the Data Base column
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200), nullable=False)
    desc=db.Column(db.String(500), nullable=False)
    date_create=db.Column(db.DateTime, default=datetime.utcnow)

    #By using this method-->display the sno and title
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET','POST'])
def hello():

    if request.method=='POST':
        # print(request.form['title'])
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

    allTodo=Todo.query.all()
    # print(allTodo)
    return render_template('index.html', allTodo=allTodo)
    # return "Hello, World!"

@app.route('/show')
def product():
    allTodo=Todo.query.all()
    print(allTodo)
    return "Working on it...! Please cheack it letter.."

@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
        
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/") #After deleting user return in again 'mysite'

if __name__=="__main__":
                    #   port=http://127.0.0.1:8000/
    app.run(debug=True, port=5000)
    # app.run(debug=True, port=5000)