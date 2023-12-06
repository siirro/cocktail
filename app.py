from flask import Flask, request, render_template, jsonify, redirect
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
    member_id = db.Column(db.ForeignKey("member.mNum"), nullable=False)
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
    member_id = db.Column(db.ForeignKey("member.mNum"), nullable=False)
    contents = db.Column(db.String, nullable=False)

    def __repr__(self):
        return


class Heart(db.Model):
    hNum = db.Column(db.Integer, primary_key=True, index=True)
    member_id = db.Column(db.ForeignKey("member.mNum"), nullable=False)
    rNum = db.Column(db.ForeignKey("recipe.rNum"), nullable=False)

    def __repr__(self):
        return


with app.app_context():
    db.create_all()



####### 조인/로그인

@app.route('/checkId', methods=['POST'])
def checkId() :
    member_id = request.json['member_id']
    id = Member.query.filter_by(member_id=member_id).first()

    if id is not None :
        return jsonify({"status" : "exist"})
    else :
        return jsonify({"status" : "available"})

@app.route("/join", methods=["GET"])
def ddd():
    return render_template("join.html")

@app.route("/join", methods=["POST"])
def join():
    
    member_id = request.form.get("member_id")
    pw = request.form.get("pw")
    nickname = request.form.get("nickname")

    member = Member(
            member_id=member_id,
            pw=pw,
            nickname=nickname
        )
    db.session.add(member)    
    db.session.commit()

    # return redirect('/')

    return render_template("join.html")

@app.route("/login", methods=["GET"])
def dddd():
    return render_template("join.html")

@app.route("/login", methods=["POST"])
def login():
    print("로그인서밋")
    return render_template("join.html")

######### 조인/로그인 끝


@app.route("/save")
def posting():
    return render_template("posting.html")


if __name__ == "__main__":
    app.run(debug=True)