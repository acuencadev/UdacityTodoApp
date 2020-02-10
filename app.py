from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Todo(db.Model):
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"<Todo {self.id} {self.description}>"


db.create_all()


@app.route('/')
def index():
    data = Todo.query.all()

    return render_template('index.html', data=data)


@app.route('/todos/create', methods=['POST'])
def create_todo():
    print(request.get_json())

    description = request.get_json()['description']
    todo = Todo(description=description)

    db.session.add(todo)
    db.session.commit()

    return jsonify({
        'description': todo.description
    })
