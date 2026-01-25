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

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reviewTitle = db.Column(db.String(100), nullable=False)
    reviewContent = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"Title : {self.reviewTitle}, Content: {self.reviewContent}"
    
class Supplement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplementName = db.Column(db.String(100), nullable=False)
    supplementDescription = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"Name {self.supplementName}, Description { self.supplementDescription}"
    
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/review")
def review():
    reviews = Review.query.all()
    return render_template("review.html", reviews=reviews)

@app.route("/add", methods=["POST"])
def add_review():
    review_title = request.form.get("review_title")
    review_content = request.form.get("review_content")

    new_review = Review(reviewTitle=review_title, reviewContent=review_content)
    db.session.add(new_review)
    db.session.commit()

    return redirect("/review")

@app.route('/delete/<int:id>')
def erase(id):
    data = Review.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/review')

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id:int):
    review = Review.query.get_or_404(id)
    if request.method == "POST":
        review.reviewTitle = request.form['review_title']
        review.reviewContent = request.form['review_content']
        try:
            db.session.commit()
            return redirect("/review")
        except Exception as e:
            return f"ERROR:{e}"
    else:
        return render_template('edit.html', review=review)
    
@app.route("/results", methods=["GET", "POST"])
def results():
    if request.method == "POST":
        search_query = request.form['searchBox']
        results = Supplement.query.filter(Supplement.supplementName.ilike(f"%{search_query}%")).all()
        return render_template('results.html', results=results)
    return redirect("/")

@app.route("/clothing")
def clothing():
    return render_template("clothing.html")
        
if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()

        s = Supplement(supplementName="Creatine", supplementDescription="Helps strength", image="creatine1.jpg")
        db.session.add(s)
        s2 = Supplement(supplementName="Micronised Creatine", supplementDescription="Muscle looks fuller", image="creatine2.jpg")
        db.session.add(s2)
        s3 = Supplement(supplementName="Creatine Gummies", supplementDescription="Easy to digest", image="creatine3.jpg")
        db.session.add(s3)
        db.session.commit()

    app.run(debug=True)