from flask import Flask, render_template, request, redirect
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)



# class Supplements(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.String(200), nullable=False)

#     def __repr__(self):
#         return f"Supplement {self.id}"

class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    threadTitle = db.Column(db.String(100), nullable=False)
    threadContent = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"Title : {self.threadTitle}, Content: {self.threadContent}"

@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/chat")
def chat():
    threads = Thread.query.all()
    return render_template("chat.html", threads=threads)

@app.route("/add", methods=["POST"])
def add_thread():
    thread_title = request.form.get("thread_title")
    thread_content = request.form.get("thread_content")

    new_thread = Thread(threadTitle=thread_title, threadContent=thread_content)
    db.session.add(new_thread)
    db.session.commit()

    return redirect("/chat")

@app.route('/delete/<int:id>')
def erase(id):
    data = Thread.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/chat')

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id:int):
    thread = Thread.query.get_or_404(id)
    if request.method == "POST":
        thread.threadContent = request.form['thread_content']
        try:
            db.session.commit()
            return redirect("/chat")
        except Exception as e:
            return f"ERROR:{e}"
    else:
        return render_template('edit.html', thread=thread)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)