from flask import Flask, request, render_template, redirect, url_for, jsonify, session
import os
from flask_sqlalchemy import SQLAlchemy
import hashlib
from datetime import timedelta
from flask_jwt_extended import JWTManager


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "database.db"
)

app.secret_key = os.urandom(24)


class Config:
    DEBUG = True
    SECRET_KEY = "QWERASDAFDSGSFDS"


app.config.from_object(Config)
jwt = JWTManager(app)
app.config["JWT_COOKIE_SECURE"] = False  # https를 통해서만 cookie가 갈수 있는지 보안망함
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]  # 토큰을 어디서 찾을지 설정
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
    hours=2
)  # 토큰 만료시간 설정 기본은 30분인데 저렇게하면 두시간인가

db = SQLAlchemy(app)


class Member(db.Model):
    mNum = db.Column(db.Integer, primary_key=True, index=True)
    member_id = db.Column(db.String, nullable=False, unique=True)
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
    # 로그인 상태를 관리하는 함수: is_admin
    id = session.get("member_id")
    print(id)

    if "member_id" in session:
        is_admin = True
    else:
        is_admin = False
    result = Member.query.filter_by(member_id=id).first()

    query = (
        db.session.query(Recipe, Member)
        .join(Member, Member.mNum == Recipe.member_id)
        .all()
    )

    searched_word = request.args.get("searched_word")
    if searched_word:
        filter_list = (
            db.session.query(Recipe, Member)
            .join(Member, Member.mNum == Recipe.member_id)
            .filter(Recipe.title == searched_word)
            .all()
        )
        db.session.commit()
        return render_template(
            "main.html", data=filter_list, is_admin=is_admin, result=result
        )
    else:
        return render_template(
            "main.html", data=query, is_admin=is_admin, result=result
        )


@app.route("/checkId", methods=["POST"])
def checkId():
    member_id = request.json["member_id"]
    id = Member.query.filter_by(member_id=member_id).first()
    if id is not None:
        return jsonify({"status": "exist"})
    else:
        return jsonify({"status": "available"})


@app.route("/join", methods=["GET"])
def ddd():
    return render_template("join.html")


@app.route("/join", methods=["POST"])
def join():
    member_id = request.form.get("member_id")
    pw = request.form.get("pw")
    pw_hash = hashlib.sha256(pw.encode("utf-8")).hexdigest()
    nickname = request.form.get("nickname")
    member = Member(member_id=member_id, pw=pw_hash, nickname=nickname)
    db.session.add(member)
    db.session.commit()
    print("회원가입DB입력완료")
    return render_template("main.html")


@app.route("/login", methods=["GET"])
def dddd():
    return render_template("join.html")


@app.route("/login", methods=["POST"])
def login():
    member_id = request.json.get("member_id")
    pw = request.json.get("pw")
    pw_hash = hashlib.sha256(pw.encode("utf-8")).hexdigest()
    result = Member.query.filter_by(member_id=member_id, pw=pw_hash).first()
    if result is not None:
        session["member_id"] = member_id
        id = session.get("member_id")
        print(id)
        # return redirect("../")
        return jsonify({"message": "ok"})
    else:
        return jsonify({"message": "아이디와 비밀번호를 확인해주세요."}), 403


@app.route("/isLogin", methods=["GET"])
def isLogin():
    if "member_id" in session:
        return jsonify({"message": "post"})
        # return render_template('posting.html')
    else:
        return jsonify({"message": "로그인 해주세요"}), 405


@app.route("/logout")
def logout():
    print("지워져라")
    if "member_id" in session:
        session.pop("member_id")
    # id = session.get('member_id')
    # print(id)
    return redirect(url_for("main"))


@app.route("/show/<int:recipeNum>")
def show(recipeNum):
    if "member_id" in session:
        is_admin = True
    else:
        is_admin = False

    id = session.get("member_id")
    print("넌 뭐냐?", id)

    recipe = Recipe.query.filter_by(rNum=recipeNum).first()
    result = Member.query.filter_by(member_id=id).first()
    comments = Comment.query.filter_by(rNum=recipeNum).all()

    instances = (
        db.session.query(Recipe, Member)
        .join(Member, Member.mNum == Recipe.member_id)
        .filter(Recipe.rNum == recipeNum)
        .all()
    )

    comments_with_authors = []
    for comment in comments:
        comment_author = Member.query.filter_by(mNum=comment.member_id).first()
        comments_with_authors.append((comment, comment_author))

    return render_template(
        "showcocktail.html",
        data=instances,
        recipe=recipe,
        comments=comments_with_authors,
        member_id=id,
        is_admin=is_admin,
        result=result,
    )


@app.route("/comment/<int:recipeNum>", methods=["POST"])
def comment(recipeNum):
    is_admin = False
    member_id = None

    id = session.get("member_id")

    if "member_id" in session:
        id = session["member_id"]
        result = Member.query.filter_by(member_id=id).first()

        if result:
            member_id = result.mNum
            is_admin = True

    if request.method == "POST":
        comment_text = request.form.get("comment")

        comment = Comment(
            rNum=recipeNum,
            member_id=member_id,
            contents=comment_text,
        )
        db.session.add(comment)
        db.session.commit()

        return redirect(url_for("show", recipeNum=recipeNum))


@app.route("/delete-comment/<int:comment_id>")
def delete_comment_new(comment_id):
    comment_to_delete = Comment.query.get(comment_id)

    if comment_to_delete:
        recipeNum = comment_to_delete.rNum  # 댓글이 속한 레시피 번호 가져오기

        db.session.delete(comment_to_delete)
        db.session.commit()

        return redirect(url_for("show", recipeNum=recipeNum))

    return redirect(url_for("main"))


@app.route("/save", methods=["GET", "POST"])
def recipe_save():
    is_admin = False
    member_id = None  # member_id 초기화

    id = session.get("member_id")

    if "member_id" in session:
        member_id = session["member_id"]
        result = Member.query.filter_by(member_id=id).first()

        if result:
            mNum = result.mNum
            is_admin = True

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
            member_id=mNum if is_admin else None,
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
        return redirect(url_for("main"))

    elif request.method == "GET":
        return render_template(
            "posting.html", data=is_admin, is_admin=is_admin, result=result
        )


@app.route("/delete/<int:recipeNum>")
def delete(recipeNum):
    recipe_delete = Recipe.query.get(recipeNum)

    if recipe_delete:
        comments_to_delete = Comment.query.filter_by(rNum=recipeNum).all()
        for comment in comments_to_delete:
            db.session.delete(comment)

        db.session.delete(recipe_delete)
        db.session.commit()

    return redirect(url_for("main"))


@app.route("/edit/<int:recipeNum>", methods=["GET", "POST"])
def edit(recipeNum):
    if "member_id" in session:
        is_admin = True
    else:
        is_admin = False

    id = session.get("member_id")

    result = Member.query.filter_by(member_id=id).first()
    recipe = Recipe.query.get(recipeNum)

    if request.method == "POST":
        # 폼에서 받은 데이터로 기존 데이터 업데이트
        recipe.title = request.form.get("title")
        recipe.image = request.form.get("image")
        recipe.ingredient = request.form.get("ingredient")
        recipe.contents1 = request.form.get("contents1")
        recipe.contents2 = request.form.get("contents2")
        recipe.contents3 = request.form.get("contents3")
        recipe.contents4 = request.form.get("contents4")
        recipe.contents5 = request.form.get("contents5")

        db.session.commit()  # 변경 사항 저장
        return redirect(url_for("show", recipeNum=recipeNum))  # 수정 후 목록 페이지로 이동

    return render_template(
        "edit.html", recipe=recipe, data=is_admin, is_admin=is_admin, result=result
    )


if __name__ == "__main__":
    app.run(debug=True)