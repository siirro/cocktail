from flask import Flask, request, render_template, redirect, url_for
import os
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "database.db"
)

db = SQLAlchemy(app)


class Member(db.Model):
    mNum = db.Column(db.Integer, primary_key=True, index=True)
    member_id = db.Column(db.String, nullable=False)
    pw = db.Column(db.String, nullable=False)
    nickname = db.Column(db.String, nullable=False)

    def __repr__(self):
        return


class Recipe(db.Model):
    rNum = db.Column(db.Integer, primary_key=True, index=True)
    member_id = db.Column(db.Integer, db.ForeignKey("member.mNum"), nullable=True)
    title = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    ingredient = db.Column(db.String, nullable=False)
    contents1 = db.Column(db.String, nullable=False)
    contents2 = db.Column(db.String, nullable=True)
    contents3 = db.Column(db.String, nullable=True)
    contents4 = db.Column(db.String, nullable=True)
    contents5 = db.Column(db.String, nullable=True)

    def __repr__(self):
        return


class Comment(db.Model):
    cNum = db.Column(db.Integer, primary_key=True, index=True)
    rNum = db.Column(db.ForeignKey("recipe.rNum"), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey("member.mNum"), nullable=False)
    contents = db.Column(db.String, nullable=False)

    def __repr__(self):
        return


class Heart(db.Model):
    hNum = db.Column(db.Integer, primary_key=True, index=True)
    member_id = db.Column(db.Integer, db.ForeignKey("member.mNum"), nullable=False)
    rNum = db.Column(db.ForeignKey("recipe.rNum"), nullable=False)

    def __repr__(self):
        return


with app.app_context():
    db.create_all()


@app.route("/")
def main():
    query = Recipe.query.all() + Member.query.all()
    return render_template("main.html", data=query)


@app.route("/join", methods=("GET", "POST"))
def join():
    return render_template("join.html")


@app.route("/show")
def show():
    # uery = db.session.query(Member)
    # query = uery.join(Recipe, Member.mNum == Recipe.member_id)
    joined_data = (
        db.session.query(Member, Recipe)
        .join(Recipe, Member.mNum == Recipe.member_id)
        .first()
    )
    print(joined_data)
    # recipe1 = Recipe.query.first()
    return render_template("showcocktail.html", data=joined_data)


@app.route("/save", methods=["GET", "POST"])
def recipe_save():
    if request.method == "POST":
        # form에서 보낸 데이터 받아오기
        title_receive = request.form.get("title")
        image_receive = request.form.get("image")
        ingredient_receive = request.form.get("ingredient")
        contents1_receive = request.form.get("contents1")
        contents2_receive = request.form.get("contents2")
        contents3_receive = request.form.get("contents3")
        contents4_receive = request.form.get("contents4")
        contents5_receive = request.form.get("contents5")

        # 데이터를 DB에 저장하기
        recipe = Recipe(
            member_id=0,
            title=title_receive,
            image=image_receive,
            ingredient=ingredient_receive,
            contents1=contents1_receive,
            contents2=contents2_receive,
            contents3=contents3_receive,
            contents4=contents4_receive,
            contents5=contents5_receive,
        )
        db.session.add(recipe)
        db.session.commit()
        return render_template("posting.html")

    elif request.method == "GET":
        return render_template("posting.html")


@app.route("/delete/<int:recipeNum>")
def delete(recipeNum):
    recipe_delete = Recipe.query.get(recipeNum)

    if recipe_delete:
        db.session.delete(recipe_delete)
        db.session.commit()

    return redirect(url_for("main.html"))


if __name__ == "__main__":
    app.run(debug=True)
