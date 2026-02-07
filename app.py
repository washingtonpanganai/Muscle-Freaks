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
    
'''
Plan
Make class for clothing
Images are going to go in here
On Clothing page the images are going to come from here
Theres going to be 3x3 pictures showing clothing
On for him there's going to be carosel of images
'''

class Clothing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clothingName = db.Column(db.String(100), nullable=False)
    clothingDescription = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(200), nullable=True)
    gender = db.Column(db.String(20), nullable=False)
    
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

@app.route("/clothing", methods=["GET"])
def clothing():
    clothes = Clothing.query.all()
    return render_template("clothing.html", clothes=clothes)

@app.route("/clothingForHim", methods=["GET"])
def clothingForHim():
    clothes = Clothing.query.filter_by(gender="male").all()
    return render_template("clothingForHim.html", clothes=clothes)

@app.route("/clothingForHer", methods=["GET"])
def clothingForHer():
    clothes = Clothing.query.filter_by(gender="female").all()
    return render_template("clothingForHer.html", clothes=clothes)

# @app.route("/clothingForHim", methods=["GET"])
# def clothingForHim():
#     clothes = Clothing.query.all()
#     return render_template("clothingForHim.html", clothes=clothes)
        
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
        

        lexClothing1 = Clothing(clothingName="Constriction Compression", clothingDescription="For the bold", image="lex.jpg", gender="male")
        db.session.add(lexClothing1)

        leanClothing1 = Clothing(clothingName="Sleek Compression", clothingDescription="For the bold", image="lean.jpg", gender="female")
        db.session.add(leanClothing1)
        
        chrisClothing1 = Clothing(clothingName="Dark Hero Compression V1", clothingDescription="For the bold", image="chris.jpg", gender="male")
        db.session.add(chrisClothing1)

        saraClothing1 = Clothing(clothingName="Sleek Compression", clothingDescription="For the bold", image="sara.jpg", gender="female")
        db.session.add(saraClothing1)
        
        mikeClothing1 = Clothing(clothingName="Dark Hero Compression V2", clothingDescription="For the bold", image="mike.jpg", gender="male")
        db.session.add(mikeClothing1)
        
        alexClothing4 = Clothing(clothingName="Relaxed Compression", clothingDescription="For the bold", image="alex2.jpg", gender="male")
        db.session.add(alexClothing4)

        lexClothing2 = Clothing(clothingName="Strong Hero Compression", clothingDescription="For the bold", image="lex3.jpg", gender="male")
        db.session.add(lexClothing2)

        chrisClothing2 = Clothing(clothingName="Slim Compression", clothingDescription="For the bold", image="chris2.jpg", gender="male")
        db.session.add(chrisClothing2)
        db.session.commit()

    app.run(debug=True)