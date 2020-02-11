import os
import sys

from flask import (abort, Flask, jsonify, redirect, render_template,
                   request, url_for)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Todo(db.Model):
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"<Todo {self.id} {self.description}>"


@app.route('/')
def index():
    data = Todo.query.all()

    return render_template('index.html', data=data)


@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}

    try:
        description = request.get_json()['description']
        todo = Todo(description=description)

        body['description'] = todo.description

        db.session.add(todo)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        abort(500)
    else:
        return jsonify({
            'description': body['description']
        })
