from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

print("Database Successfully Connected To Flask")


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    due_date = db.Column(db.DateTime(), nullable=False)
    status = db.Column(db.String(100), nullable=False)


@app.route("/")
def root():
    return "Hello"


@app.route("/home")
def home():
    todos = Todo.query.all()

    if request.method == "POST":
        name = request.form.get("todo-name")
        date = request.form.get("todo-date")
        status = request.form.get("todo-status")

        print(name, date, status)

        return name

    else:
        return render_template("index.html", todos=todos)


@app.route("/add", methods=["POST"])
def add_todo():

    todo_name = request.form.get("todo-name")
    todo_dueDate = request.form.get("todo-date")
    todo_status = request.form.get("todo-status")

    todo_dueDate = datetime.strptime(todo_dueDate, "%Y-%m-%d")

    t1 = Todo(
        name=todo_name,
        due_date=todo_dueDate,
        status=todo_status
    )

    db.session.add(t1)
    db.session.commit()

    return redirect("/home")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_todo(id):

    todo = Todo.query.get_or_404(id)

    if request.method == "POST":

        todo.name = request.form.get("todo-name")
        date = request.form.get("todo-date")

        if date:
            todo.due_date = datetime.strptime(date, "%Y-%m-%d")

        todo.status = request.form.get("todo-status")
        db.session.commit()

        return redirect("/home")

    return render_template("edit.html", todo=todo)

@app.route("/delete/<int:id>", methods=["POST"])
def delete_todo(id):

    todo = Todo.query.get_or_404(id)

    db.session.delete(todo)
    db.session.commit()

    return redirect("/home")


@app.route("/get", methods=["GET"])
def get_todo():

    todos = Todo.query.all()

    return render_template(
        "index.html",
        todos=todos,
        show_todos=True
    )

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)


