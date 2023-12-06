from flask import Flask, render_template
app = Flask(__name__)

# SQLite3 설정
import os
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)

############################ 테이블 생성
class Member(db.Model):
    id = db.Column(db.String, primary_key=True)
    pw = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return
    
class Recipe(db.Model):
    rNum = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.ForeignKey('member.id'), nullable=False)
    title = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    contents = db.Column(db.String, nullable=False)
    ingredient = db.Column(db.String, nullable=False)

    def __repr__(self):
        return
    
class Comment(db.Model):
    cNum = db.Column(db.Integer, primary_key=True)
    rNum = db.Column(db.ForeignKey('recipe.rNum'), nullable=False)
    id = db.Column(db.ForeignKey('member.id'), nullable=False)
    contents = db.Column(db.String, nullable=False)

    def __repr__(self):
        return

class Heart(db.Model):
    hNum = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.ForeignKey('member.id'), nullable=False)
    rNum = db.Column(db.ForeignKey('recipe.rNum'), nullable=False)
    
    def __repr__(self):
        return

with app.app_context():
    db.create_all()

############################# 테이블 생성 끝



# 로그인/회원가입 #####################################
@app.route('/join', methods=('GET', 'POST'))
def join():

    
    return render_template('join.html')

















# 로그인/회원가입 #####################################


if __name__ == '__main__':
    app.run(debug=True)