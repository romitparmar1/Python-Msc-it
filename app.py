
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Date
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(Integer, primary_key=True)
    title = db.Column(String(200), nullable=False)
    description = db.Column(String(200), nullable=False)
    priority = db.Column(String(200), nullable=False)
    is_complited = db.Column(String(5), nullable=False)
    due_date = db.Column(Date, nullable=False)


@app.route("/")
def home():
    return render_template("index.html", data=Todo.query.order_by(Todo.id.desc()).all())


@app.route("/add", methods=["POST"])
def add_todo():
    title = request.form.get("title")
    description = request.form.get("description")
    priority = request.form.get("priority")
    is_completed = request.form.get("is_complited", "False")
    due_date = request.form.get("due_date")

    due_date = datetime.strptime(due_date, "%Y-%m-%d").date()

    new_todo = Todo(
        title=title,
        description=description,
        priority=priority,
        is_complited=is_completed,
        due_date=due_date
    )

    db.session.add(new_todo)
    db.session.commit()

    return redirect(url_for("home"))


@app.route("/get", methods=["GET"])
def get_todo():
    todo_list = Todo.query.order_by(Todo.id.desc()).all()
    return render_template("index.html", data=todo_list)


@app.route("/toggle/<int:id>")
def toggle_todo(id):
    todo = db.session.get(Todo, id)

    if todo:
        todo.is_complited = (
            "False" if todo.is_complited == "True" else "True"
        )
        db.session.commit()

    return redirect(url_for("get_todo"))


@app.route("/edit", methods=["GET", "POST"])
def edit_todo():
    if request.method == "GET":
        e_id = request.args.get("e_id", type=int)
        todo = db.session.get(Todo, e_id)

        if todo is None:
            return redirect(url_for("get_todo"))

        return render_template("edit_todo.html", t1=todo)

    e_id = request.form.get("e_id", type=int)
    todo = db.session.get(Todo, e_id)

    if todo is None:
        return redirect(url_for("get_todo"))

    todo.title = request.form.get("e_title")
    todo.description = request.form.get("e_description")
    todo.priority = request.form.get("e_priority")
    todo.is_complited = request.form.get("e_is_completed", "False")

    due_date = request.form.get("e_due_date")
    todo.due_date = datetime.strptime(due_date, "%Y-%m-%d").date()

    db.session.commit()

    return redirect(url_for("get_todo"))


@app.route("/delete", methods=["POST"])
def delete_todo():
    d_id = request.form.get("d_id", type=int)
    todo = db.session.get(Todo, d_id)

    if todo:
        db.session.delete(todo)
        db.session.commit()

    return redirect(url_for("get_todo"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)