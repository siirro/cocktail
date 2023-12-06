from flask import Flask, request, render_template, jsonify
import os
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "database.db"
)

db = SQLAlchemy(app)


class Recipe(db.Model):
    recipe_num = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    ingredient = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"{self.artist} {self.title} 추천 by {self.username}"


with app.app_context():
    db.create_all()


@app.route("/posting")
def posting():
    return render_template("posting.html")


if __name__ == "__main__":
    app.run(debug=True)
