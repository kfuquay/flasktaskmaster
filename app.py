from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# config database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# initialize database
db = SQLAlchemy(app)

# database setup


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # content less than 200 chars, cannot be blank
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

# in terminal - to setup db -
# 1. python3
# 2. from app import db
# 3. db.create_all()
# 4. check to see if .db file appears in project folder
# 5. exit()


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # create a model todo object
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        # push it to db
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        # query db, get all todos ordered by date
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

# Delete route
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting the task'

# Update route
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem updating the task'
    else:
        return render_template('update.html', task=task)


if __name__ == '__main__':
    app.run(debug=True)

## to deploy to heroku
# pip3 install gunicorn
# freeze requirements
# pip3 freeze > requirements.txt
# make git repo, commit
# touch Procfile
# web: gunicorn app:app
# heroku create ~application name~
# git remove -v 
# git push heroku master

